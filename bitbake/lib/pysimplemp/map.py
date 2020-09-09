#! /usr/bin/env python3
# Copyright (c) 2020 Joshua Watt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Provides a map()-like interface that does the work in a pool of worker
# threads. Unlike a traditional map() or worker pool, the about of work must be
# fixed when the pool is created (e.g. a list, not an iterable). The work will
# be divide between the worker processes. The pool is guaranteed to be safe to
# terminate at any point without deadlocking.

import contextlib
import multiprocessing
import os
import signal
import sys
import time
from .errors import ResultQueueEmpty
from .util import sigmask


class MapResult(object):
    def __init__(self, is_exception, result, job_idx):
        self.is_exception = is_exception
        self.result = result
        self.job_idx = job_idx

    def get(self):
        if self.is_exception:
            raise self.result
        return self.result


class MapPool(object):
    MAX_WORKERS = 100000
    STATE_READY = -1
    STATE_READING_RESULT = -3
    STATE_FINISHED = -4
    STATE_IN_PROGRESS = MAX_WORKERS
    STATE_QUEUEING_RESULT = STATE_IN_PROGRESS + MAX_WORKERS

    @classmethod
    def get_in_progress_worker(self, v):
        if v >= self.STATE_IN_PROGRESS and v < self.STATE_QUEUEING_RESULT:
            return v - self.STATE_IN_PROGRESS
        return None

    @classmethod
    def get_queueing_result_worker(self, v):
        if v >= self.STATE_QUEUEING_RESULT:
            return v - self.STATE_QUEUEING_RESULT
        return None

    def __init__(
        self,
        func,
        jobs,
        num_processes=None,
        interruptable=True,
        init=None,
        deinit=None,
        ctx=None,
    ):
        """
        Create a new pool of worker threads to apply `func` to each item of
        `jobs`. All jobs must be know when the pool is created so `jobs` will
        be converted to a `list`

        The number of worker processes is controlled by the `num_processes`
        argument. If unspecified, `multiprocess.cpu_count()` will be used

        If `interruptable` is `True` (the default), `func` can be interrupted
        when `join()` is called on the pool. Otherwise, the worker thread will
        not terminated until `func` has completed. Care must be taken when
        using this option, as `join()` may wait forever if `func` never exits.

        `init` specifies a function to run once when the worker thread is
        initialized, and is guaranteed to run, even if the worker process is
        terminated with `join()`

        `deinit` specifies a function to run when the worker thread terminates.
        It is guaranteed to as long as `init` does not raise an exception

        `ctx` is the multiprocessing context to use, or
        `multiprocessing.get_context()` if unspecified

        The pool may be used as a context manager which will automatically call
        `start()` and `join()`::

            with MapPool(foo, jobs) as p:
                r = p.results()

        is equivalent to::

            p = MapPool(foo, jobs)
            try:
                p.start()
                r = p.results()
            finally:
                p.terminate()
                p.join()
        """
        self.jobs = list(jobs)
        self.func = func
        self.ctx = ctx or multiprocessing.get_context()
        self.interruptable = interruptable

        self.result_queues = []
        self.result_semaphore = self.ctx.Semaphore(0)
        self.processes = []
        self.num_processes = num_processes or multiprocessing.cpu_count()
        self.init = init
        self.deinit = deinit

        # Track the state of each job. The state can be one of the following
        # values:
        #   STATE_READY       - No worker has started processing the job yet
        #   STATE_IN_PROGRESS - worker is currently processing the job
        #   Any integer >= 0  - The worker process with the specified index has
        #                       completed the job and may be waiting to write
        #                       the result back
        #   STATE_READING_RESULT  - The result is being read from the worker's
        #                           queue by the main process
        #   STATE_FINISHED    - The main process has read the result from the
        #                       worker's result queue
        self.states = self.ctx.Array("i", [self.STATE_READY] * len(self.jobs))

    @contextlib.contextmanager
    def _sigblock(self):
        # Helper function to block SIGTERM
        with sigmask(signal.SIG_BLOCK, [signal.SIGTERM]):
            yield

    def _child_worker(self, worker_idx, queue):
        def do_exit(*args, **kwargs):
            if self.deinit:
                self.deinit()
            os._exit(0)

        try:
            if self.init:
                self.init()
        except:
            os._exit(1)

        signal.signal(signal.SIGTERM, do_exit)

        # This thread is ready to be terminated. Unblock SIGTERM inherited from
        # parent
        signal.pthread_sigmask(signal.SIG_UNBLOCK, [signal.SIGTERM])


        while True:
            # Look for a job to process and reserve one if found. Block the
            # termination signal to ensure that this is atomic and the process
            # isn't killed with the array lock held
            job_index = None
            with self._sigblock(), self.states.get_lock():
                for idx, state, _ in self._each_state():
                    if state == self.STATE_READY:
                        job_index = idx
                        self.states[idx] = self.STATE_IN_PROGRESS + worker_idx
                        break

            if job_index is None:
                # No work left to do
                do_exit()
                break

            if self.interruptable:
                mask = []
            else:
                mask = [signal.SIGTERM]

            try:
                with sigmask(signal.SIG_BLOCK, mask):
                    result = MapResult(
                        False, self.func(*self.jobs[job_index]), job_index
                    )
            except Exception as e:
                result = MapResult(True, e, job_index)

            with self._sigblock():
                # Mark the job as ready to be received by the main process
                with self.states.get_lock():
                    self.states[job_index] = self.STATE_QUEUEING_RESULT + worker_idx

                # Signal there is an item ready to be processed
                self.result_semaphore.release()

                queue.put(result)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.terminate()
        self.join()

    def _each_state(self):
        for idx in range(len(self.states)):
            (state, worker_idx) = self._get_state(idx)
            yield idx, state, worker_idx

    def _get_state(self, idx):
        v = self.states[idx]

        if v >= self.STATE_IN_PROGRESS and v < self.STATE_QUEUEING_RESULT:
            return (self.STATE_IN_PROGRESS, v - self.STATE_IN_PROGRESS)

        if v >= self.STATE_QUEUEING_RESULT:
            return (self.STATE_QUEUEING_RESULT, v - self.STATE_QUEUEING_RESULT)

        return (v, None)

    def results(self, block=True):
        """
        An iterator that gets the mapping results from the worker pool. The
        results may be returned in any order.

        If any job raised an exception in the worker, it will be raised when in
        the parent process when its result would be returned

        If `block` is `True` (the default), the function will block until
        a result is ready or there are no more results left
        """
        try:
            while True:
                yield self.get(block)
        except ResultQueueEmpty:
            pass

    def results_ordered(self, block=True):
        """
        An iterator that gets the mapping results from the worker pool. The
        results are returned in the same order as they are listed in the job
        list.

        If any job raised an exception in the worker, it will be raised when in
        the parent process when its result would be returned

        If `block` is `True` (the default), the function will block until
        a result is ready or there are no more results left
        """
        results = {}
        for i in range(len(self.jobs)):
            try:
                while not i in results:
                    result = self._get(block)
                    results[result.job_idx] = result
            except ResultQueueEmpty:
                pass

            if i in results:
                yield results[i].get()
            else:
                break

    def start(self):
        """
        Starts the worker pool. This must be called to create the worker pool
        and have the workers start processing jobs.

        `join()` must be called after this to clean up the worker pool.
        """
        # Flush to prevent duplication in worker processes
        sys.stdout.flush()
        sys.stderr.flush()

        # Block signals. The worker processes will inherit this signal mask,
        # which ensures that they cannot terminate before they have initialized
        with self._sigblock():
            self.result_queues = []
            self.processes = []

            for i in range(self.num_processes):
                queue = self.ctx.SimpleQueue()

                pid = os.fork()
                if pid == 0:
                    self._child_worker(i, queue)
                    os._exit(0)
                else:
                    self.processes.append(pid)
                    self.result_queues.append(queue)

    def _get(self, block):
        # There a small race where join() may read items out of a result queue
        # before this code can change the state to STATE_READING_RESULT to
        # "reserve" it. In this case, the code needs to loop again (which will
        # most likely result in all states being STATE_FINISHED and raising
        # ResultQueueEmpty()). Not that for this to happen, join() must be
        # called on from a thread other than the one processing results.
        while True:
            # Find the queue that has the result, and mark is as being read
            is_finished = True
            worker_idx = None

            with self.states.get_lock():
                for idx, state, widx in self._each_state():
                    if state == self.STATE_QUEUEING_RESULT:
                        worker_idx = widx
                        self.states[idx] = self.STATE_READING_RESULT
                        break
                    elif state != self.STATE_FINISHED:
                        is_finished = False
                else:
                    # If we didn't find a worker and all jobs are finished,
                    # raise the queue empty exception
                    if is_finished:
                        raise ResultQueueEmpty()

            if worker_idx is not None:
                break

            # Wait for any result to be ready
            if not self.result_semaphore.acquire(block):
                raise ResultQueueEmpty()

        result = self.result_queues[worker_idx].get()

        # Mark job as finished
        with self.states.get_lock():
            self.states[result.job_idx] = self.STATE_FINISHED

        return result

    def get(self, block=True):
        """
        Gets the next available result from the  worker pool. Either returns
        the result of the function, or raises an exception if one was raised in
        the worker process. If there are no more results to be returned, a
        `ResultQueueEmpty` exception is raised.

        Results may be returned in any order.

        If `block` is `True` (the default), the function will block until
        a result is ready or there are no more results left. If `False` and the
        function would block, a `ResultQueueEmpty` exception is raised.
        """
        return self._get(block).get()

    def terminate(self):
        """
        Terminate all worker processes. This must be called before `join()`
        """
        for p in self.processes:
            os.kill(p, signal.SIGTERM)

    def join(self):
        """
        Wait for all worker processes to exit. This must be called to cleanup
        all the worker processes when finished.

        Any results that have not been collected will be lost
        """

        wait_pids = set(self.processes)

        while True:
            queue_reads = []
            in_process_pids = set()

            with self.states.get_lock():
                for idx, state, worker_idx in self._each_state():
                    if state == self.STATE_QUEUEING_RESULT:
                        # Workers block the terminate signal while writing to
                        # their result queue. If they are blocked waiting for
                        # data to be read out of the queue, they will not be
                        # able to receive the terminate signal. Find all tasks
                        # that cannot get the signal because it is blocked and
                        # read their result queue to unblock them so they can
                        # terminate
                        self.result_queues[worker_idx].get()
                        self.states[idx] = self.STATE_FINISHED
                    elif state == self.STATE_IN_PROGRESS:
                        # If this worker is still in progress, there are a few
                        # possible options:
                        # 1) The worker is still executing it's job (which may be
                        #   uninterruptable)
                        # 2) The worker has exited
                        # 3) The worker has signals disabled and is waiting for the
                        #   states lock to change the state to QUEUEING_RESULT
                        #
                        # If we detect a process in this state, do a non-blocking
                        # wait with the locks released to try and
                        in_process_pids.add(self.processes[worker_idx])
                    elif state == self.STATE_READY:
                        self.states[idx] = self.STATE_FINISHED

            new_wait_pids = set()
            for pid in wait_pids:
                (wait_pid, status) = os.waitpid(
                    pid, os.WNOHANG if pid in in_process_pids else 0
                )
                if (wait_pid, status) == (0, 0):
                    new_wait_pids.add(pid)

            if not new_wait_pids:
                # No processes still pending.
                break

            wait_pids = new_wait_pids
            time.sleep(0.1)
