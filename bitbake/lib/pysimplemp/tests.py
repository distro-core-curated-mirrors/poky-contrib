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

import multiprocessing
import random
import time
import unittest
from . import MapPool, ResultQueueEmpty


class TestJobException(Exception):
    def __init__(self, job_num):
        self.job_num = job_num


class MapPoolTests(unittest.TestCase):
    HUGE_SIZE = 1024 * 1024

    def test_results(self):
        def func(job_num):
            time.sleep(1 + random.random())
            return job_num

        jobs = [(i,) for i in range(multiprocessing.cpu_count() * 5)]

        seen = [False for i in range(len(jobs))]
        with MapPool(func, jobs) as p:
            for r in p.results():
                self.assertFalse(seen[r], "Job index %d already seen!" % r)
                seen[r] = True

        for idx, r in enumerate(seen):
            self.assertTrue(r, "No results for job %d" % idx)

    def test_results_ordered(self):
        def func(job_num):
            time.sleep(1 + random.random())
            return job_num

        jobs = [(i,) for i in range(multiprocessing.cpu_count() * 5)]

        with MapPool(func, jobs) as p:
            count = 0
            for idx, r in enumerate(p.results_ordered()):
                count += 1
                self.assertEqual(r, idx, "Index received out of order")

            self.assertEqual(count, len(jobs), "Incorrect number of jobs received")

    def test_exception(self):
        def func(job_num):
            raise TestJobException(job_num)

        jobs = [(i,) for i in range(multiprocessing.cpu_count() * 5)]

        seen = [False for i in range(len(jobs))]
        with MapPool(func, jobs) as p:
            while True:
                with self.assertRaises((TestJobException, ResultQueueEmpty)) as e:
                    p.get()

                if isinstance(e.exception, ResultQueueEmpty):
                    break
                seen[e.exception.job_num] = True

        for idx, r in enumerate(seen):
            self.assertTrue(r, "No exception for job %d" % idx)

    def test_huge(self):
        def func(job_num):
            time.sleep(1 + random.random())
            return [job_num] * self.HUGE_SIZE

        jobs = [(i,) for i in range(multiprocessing.cpu_count() * 5)]

        with MapPool(func, jobs) as p:
            for r in p.results():
                self.assertEqual(len(r), self.HUGE_SIZE, "Job returned incorrect size")

    def test_stress(self):
        def func(job_num):
            time.sleep(random.random() / multiprocessing.cpu_count())
            return job_num

        jobs = [(i,) for i in range(multiprocessing.cpu_count() * 10)]

        for i in range(100):
            with MapPool(func, jobs, interruptable=False) as p:
                time.sleep(1)

    def test_huge_interrupt(self):
        # Test that joining works even if the child processes are waiting to
        # write to their queues
        def func(job_num):
            return [job_num] * self.HUGE_SIZE

        jobs = [(i,) for i in range(multiprocessing.cpu_count() * 5)]

        with MapPool(func, jobs, interruptable=False) as p:
            time.sleep(1)

    def test_init(self):
        def func():
            pass

        def init():
            nonlocal init_count
            with init_count.get_lock():
                init_count.value += 1

        num_processes = 10

        jobs = [tuple for i in range(num_processes * 5)]

        init_count = multiprocessing.Value("i", 0)

        with MapPool(func, jobs, init=init, num_processes=num_processes) as p:
            pass

        self.assertEqual(init_count.value, num_processes)

    def test_deinit(self):
        def func():
            pass

        def deinit():
            nonlocal deinit_count
            with deinit_count.get_lock():
                deinit_count.value += 1

        num_processes = 10

        jobs = [tuple for i in range(num_processes * 5)]

        deinit_count = multiprocessing.Value("i", 0)

        with MapPool(func, jobs, deinit=deinit, num_processes=num_processes) as p:
            pass

        self.assertEqual(deinit_count.value, num_processes)

    def test_deinit_skipped(self):
        # Tests that deinit() is skipped it init() raises an exception
        def func():
            pass

        def init():
            raise Exception("Skipping deinit")

        def deinit():
            nonlocal deinit_count
            with deinit_count.get_lock():
                deinit_count.value += 1

        num_processes = 10

        jobs = [tuple for i in range(num_processes * 5)]

        deinit_count = multiprocessing.Value("i", 0)

        with MapPool(
            func, jobs, init=init, deinit=deinit, num_processes=num_processes
        ) as p:
            pass

        self.assertEqual(deinit_count.value, 0)


if __name__ == "__main__":
    unittest.main()
