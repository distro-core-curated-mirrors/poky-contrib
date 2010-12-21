#!/usr/bin/env python
# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
"""
BitBake 'RunQueue' implementation

Handles preparation and execution of a queue of tasks
"""

# Copyright (C) 2006-2007  Richard Purdie
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import bb, os, sys
import subprocess
from bb import msg, data, event, parse
import signal
import stat
import fcntl
import copy

try:
    import cPickle as pickle
except ImportError:
    import pickle
    bb.msg.note(1, bb.msg.domain.Cache, "Importing cPickle failed. Falling back to a very slow implementation.")

class RunQueueStats:
    """
    Holds statistics on the tasks handled by the associated runQueue
    """
    def __init__(self, total):
        self.completed = 0
        self.skipped = 0
        self.failed = 0
        self.active = 0
        self.total = total

    def taskFailed(self):
        self.active = self.active - 1
        self.failed = self.failed + 1

    def taskCompleted(self, number = 1):
        self.active = self.active - number
        self.completed = self.completed + number

    def taskSkipped(self, number = 1):
        self.active = self.active + number
        self.skipped = self.skipped + number

    def taskActive(self):
        self.active = self.active + 1

# These values indicate the next step due to be run in the
# runQueue state machine
runQueuePrepare = 2
runQueueSceneInit = 3
runQueueSceneRun = 4
runQueueRunInit = 5
runQueueRunning = 6
runQueueFailed = 7
runQueueCleanUp = 8
runQueueComplete = 9
runQueueChildProcess = 10

class RunQueueScheduler(object):
    """
    Control the order tasks are scheduled in.
    """
    name = "basic"

    def __init__(self, runqueue, rqdata):
        """
        The default scheduler just returns the first buildable task (the
        priority map is sorted by task numer)
        """
        self.rq = runqueue
        self.rqdata = rqdata
        numTasks = len(self.rq.runq_fnid)

        self.prio_map = []
        self.prio_map.extend(range(numTasks))

    def next(self):
        """
        Return the id of the first task we find that is buildable
        """
        for task1 in range(len(self.rqdata.runq_fnid)):
            task = self.prio_map[task1]
            if self.rq.runq_running[task] == 1:
                continue
            if self.rq.runq_buildable[task] == 1:
                return task

class RunQueueSchedulerSpeed(RunQueueScheduler):
    """
    A scheduler optimised for speed. The priority map is sorted by task weight,
    heavier weighted tasks (tasks needed by the most other tasks) are run first.
    """
    name = "speed"

    def __init__(self, runqueue, rqdata):
        """
        The priority map is sorted by task weight.
        """
        from copy import deepcopy

        self.rq = runqueue
        self.rqdata = rqdata

        sortweight = sorted(deepcopy(self.rqdata.runq_weight))
        copyweight = deepcopy(self.rqdata.runq_weight)
        self.prio_map = []

        for weight in sortweight:
            idx = copyweight.index(weight)
            self.prio_map.append(idx)
            copyweight[idx] = -1

        self.prio_map.reverse()

class RunQueueSchedulerCompletion(RunQueueSchedulerSpeed):
    """
    A scheduler optimised to complete .bb files are quickly as possible. The
    priority map is sorted by task weight, but then reordered so once a given
    .bb file starts to build, its completed as quickly as possible. This works
    well where disk space is at a premium and classes like OE's rm_work are in
    force.
    """
    name = "completion"

    def __init__(self, runqueue, rqdata):
        RunQueueSchedulerSpeed.__init__(self, runqueue, rqdata)
        from copy import deepcopy

        #FIXME - whilst this groups all fnids together it does not reorder the
        #fnid groups optimally.

        basemap = deepcopy(self.prio_map)
        self.prio_map = []
        while (len(basemap) > 0):
            entry = basemap.pop(0)
            self.prio_map.append(entry)
            fnid = self.rqdata.runq_fnid[entry]
            todel = []
            for entry in basemap:
                entry_fnid = self.rqdata.runq_fnid[entry]
                if entry_fnid == fnid:
                    todel.append(basemap.index(entry))
                    self.prio_map.append(entry)
            todel.reverse()
            for idx in todel:
                del basemap[idx]

class RunQueueData:
    """
    BitBake Run Queue implementation
    """
    def __init__(self, rq, cooker, cfgData, dataCache, taskData, targets):
        self.cooker = cooker
        self.dataCache = dataCache
        self.taskData = taskData
        self.targets = targets
        self.rq = rq

        self.stampwhitelist = bb.data.getVar("BB_STAMP_WHITELIST", cfgData, 1) or ""
        self.multi_provider_whitelist = (bb.data.getVar("MULTI_PROVIDER_WHITELIST", cfgData, 1) or "").split()

        self.reset()

    def reset(self):
        self.runq_fnid = []
        self.runq_task = []
        self.runq_depends = []
        self.runq_revdeps = []
        self.runq_hash = []

    def runq_depends_names(self, ids):
        import re
        ret = []
        for id in self.runq_depends[ids]:
            nam = os.path.basename(self.get_user_idstring(id))
            nam = re.sub("_[^,]*,", ",", nam)
            ret.extend([nam])
        return ret

    def get_user_idstring(self, task):
        fn = self.taskData.fn_index[self.runq_fnid[task]]
        taskname = self.runq_task[task]
        return "%s, %s" % (fn, taskname)

    def get_task_id(self, fnid, taskname):
        for listid in range(len(self.runq_fnid)):
            if self.runq_fnid[listid] == fnid and self.runq_task[listid] == taskname:
                return listid
        return None

    def circular_depchains_handler(self, tasks):
        """
        Some tasks aren't buildable, likely due to circular dependency issues.
        Identify the circular dependencies and print them in a user readable format.
        """
        from copy import deepcopy

        valid_chains = []
        explored_deps = {}
        msgs = []

        def chain_reorder(chain):
            """
            Reorder a dependency chain so the lowest task id is first
            """
            lowest = 0
            new_chain = []
            for entry in range(len(chain)):
                if chain[entry] < chain[lowest]:
                    lowest = entry
            new_chain.extend(chain[lowest:])
            new_chain.extend(chain[:lowest])
            return new_chain

        def chain_compare_equal(chain1, chain2):
            """
            Compare two dependency chains and see if they're the same
            """
            if len(chain1) != len(chain2):
                return False
            for index in range(len(chain1)):
                if chain1[index] != chain2[index]:
                    return False
            return True

        def chain_array_contains(chain, chain_array):
            """
            Return True if chain_array contains chain
            """
            for ch in chain_array:
                if chain_compare_equal(ch, chain):
                    return True
            return False

        def find_chains(taskid, prev_chain):
            prev_chain.append(taskid)
            total_deps = []
            total_deps.extend(self.runq_revdeps[taskid])
            for revdep in self.runq_revdeps[taskid]:
                if revdep in prev_chain:
                    idx = prev_chain.index(revdep)
                    # To prevent duplicates, reorder the chain to start with the lowest taskid
                    # and search through an array of those we've already printed
                    chain = prev_chain[idx:]
                    new_chain = chain_reorder(chain)
                    if not chain_array_contains(new_chain, valid_chains):
                        valid_chains.append(new_chain)
                        msgs.append("Dependency loop #%d found:\n" % len(valid_chains))
                        for dep in new_chain:
                            msgs.append("  Task %s (%s) (dependent Tasks %s)\n" % (dep, self.get_user_idstring(dep), self.runq_depends_names(dep)))
                        msgs.append("\n")
                    if len(valid_chains) > 10:
                        msgs.append("Aborted dependency loops search after 10 matches.\n")
                        return msgs
                    continue
                scan = False
                if revdep not in explored_deps:
                    scan = True
                elif revdep in explored_deps[revdep]:
                    scan = True
                else:
                    for dep in prev_chain:
                        if dep in explored_deps[revdep]:
                            scan = True
                if scan:
                    find_chains(revdep, deepcopy(prev_chain))
                for dep in explored_deps[revdep]:
                    if dep not in total_deps:
                        total_deps.append(dep)

            explored_deps[taskid] = total_deps

        for task in tasks:
            find_chains(task, [])

        return msgs

    def calculate_task_weights(self, endpoints):
        """
        Calculate a number representing the "weight" of each task. Heavier weighted tasks
        have more dependencies and hence should be executed sooner for maximum speed.

        This function also sanity checks the task list finding tasks that its not
        possible to execute due to circular dependencies.
        """

        numTasks = len(self.runq_fnid)
        weight = []
        deps_left = []
        task_done = []

        for listid in range(numTasks):
            task_done.append(False)
            weight.append(0)
            deps_left.append(len(self.runq_revdeps[listid]))

        for listid in endpoints:
            weight[listid] = 1
            task_done[listid] = True

        while True:
            next_points = []
            for listid in endpoints:
                for revdep in self.runq_depends[listid]:
                    weight[revdep] = weight[revdep] + weight[listid]
                    deps_left[revdep] = deps_left[revdep] - 1
                    if deps_left[revdep] == 0:
                        next_points.append(revdep)
                        task_done[revdep] = True
            endpoints = next_points
            if len(next_points) == 0:
                break

        # Circular dependency sanity check
        problem_tasks = []
        for task in range(numTasks):
            if task_done[task] is False or deps_left[task] != 0:
                problem_tasks.append(task)
                bb.msg.debug(2, bb.msg.domain.RunQueue, "Task %s (%s) is not buildable\n" % (task, self.get_user_idstring(task)))
                bb.msg.debug(2, bb.msg.domain.RunQueue, "(Complete marker was %s and the remaining dependency count was %s)\n\n" % (task_done[task], deps_left[task]))

        if problem_tasks:
            message = "Unbuildable tasks were found.\n"
            message = message + "These are usually caused by circular dependencies and any circular dependency chains found will be printed below. Increase the debug level to see a list of unbuildable tasks.\n\n"
            message = message + "Identifying dependency loops (this may take a short while)...\n"
            bb.msg.error(bb.msg.domain.RunQueue, message)

            msgs = self.circular_depchains_handler(problem_tasks)

            message = "\n"
            for msg in msgs:
                message = message + msg
            bb.msg.fatal(bb.msg.domain.RunQueue, message)

        return weight

    def prepare(self):
        """
        Turn a set of taskData into a RunQueue and compute data needed
        to optimise the execution order.
        """

        runq_build = []
        recursive_tdepends = {}
        runq_recrdepends = []
        tdepends_fnid = {}

        taskData = self.taskData

        if len(taskData.tasks_name) == 0:
            # Nothing to do
            return 0

        bb.msg.note(1, bb.msg.domain.RunQueue, "Preparing runqueue")

        # Step A - Work out a list of tasks to run
        #
        # Taskdata gives us a list of possible providers for every build and run
        # target ordered by priority. It also gives information on each of those
        # providers.
        #
        # To create the actual list of tasks to execute we fix the list of
        # providers and then resolve the dependencies into task IDs. This
        # process is repeated for each type of dependency (tdepends, deptask,
        # rdeptast, recrdeptask, idepends).

        def add_build_dependencies(depids, tasknames, depends):
            for depid in depids:
                # Won't be in build_targets if ASSUME_PROVIDED
                if depid not in taskData.build_targets:
                    continue
                depdata = taskData.build_targets[depid][0]
                if depdata is None:
                    continue
                dep = taskData.fn_index[depdata]
                for taskname in tasknames:
                    taskid = taskData.gettask_id(dep, taskname, False)
                    if taskid is not None:
                        depends.append(taskid)

        def add_runtime_dependencies(depids, tasknames, depends):
            for depid in depids:
                if depid not in taskData.run_targets:
                    continue
                depdata = taskData.run_targets[depid][0]
                if depdata is None:
                    continue
                dep = taskData.fn_index[depdata]
                for taskname in tasknames:
                    taskid = taskData.gettask_id(dep, taskname, False)
                    if taskid is not None:
                        depends.append(taskid)

        for task in range(len(taskData.tasks_name)):
            depends = []
            recrdepends = []
            fnid = taskData.tasks_fnid[task]
            fn = taskData.fn_index[fnid]
            task_deps = self.dataCache.task_deps[fn]

            bb.msg.debug(2, bb.msg.domain.RunQueue, "Processing %s:%s" %(fn, taskData.tasks_name[task]))

            if fnid not in taskData.failed_fnids:

                # Resolve task internal dependencies
                #
                # e.g. addtask before X after Y
                depends = taskData.tasks_tdepends[task]

                # Resolve 'deptask' dependencies
                #
                # e.g. do_sometask[deptask] = "do_someothertask"
                # (makes sure sometask runs after someothertask of all DEPENDS)
                if 'deptask' in task_deps and taskData.tasks_name[task] in task_deps['deptask']:
                    tasknames = task_deps['deptask'][taskData.tasks_name[task]].split()
                    add_build_dependencies(taskData.depids[fnid], tasknames, depends)

                # Resolve 'rdeptask' dependencies
                #
                # e.g. do_sometask[rdeptask] = "do_someothertask"
                # (makes sure sometask runs after someothertask of all RDEPENDS)
                if 'rdeptask' in task_deps and taskData.tasks_name[task] in task_deps['rdeptask']:
                    taskname = task_deps['rdeptask'][taskData.tasks_name[task]]
                    add_runtime_dependencies(taskData.rdepids[fnid], [taskname], depends)

                # Resolve inter-task dependencies
                #
                # e.g. do_sometask[depends] = "targetname:do_someothertask"
                # (makes sure sometask runs after targetname's someothertask)
                if fnid not in tdepends_fnid:
                    tdepends_fnid[fnid] = set()
                idepends = taskData.tasks_idepends[task]
                for (depid, idependtask) in idepends:
                    if depid in taskData.build_targets:
                        # Won't be in build_targets if ASSUME_PROVIDED
                        depdata = taskData.build_targets[depid][0]
                        if depdata is not None:
                            dep = taskData.fn_index[depdata]
                            taskid = taskData.gettask_id(dep, idependtask)
                            depends.append(taskid)
                            if depdata != fnid:
                                tdepends_fnid[fnid].add(taskid)


                # Resolve recursive 'recrdeptask' dependencies (A)
                #
                # e.g. do_sometask[recrdeptask] = "do_someothertask"
                # (makes sure sometask runs after someothertask of all DEPENDS, RDEPENDS and intertask dependencies, recursively)
                # We cover the recursive part of the dependencies below
                if 'recrdeptask' in task_deps and taskData.tasks_name[task] in task_deps['recrdeptask']:
                    for taskname in task_deps['recrdeptask'][taskData.tasks_name[task]].split():
                        recrdepends.append(taskname)
                        add_build_dependencies(taskData.depids[fnid], [taskname], depends)
                        add_runtime_dependencies(taskData.rdepids[fnid], [taskname], depends)

                # Rmove all self references
                if task in depends:
                    newdep = []
                    bb.msg.debug(2, bb.msg.domain.RunQueue, "Task %s (%s %s) contains self reference! %s" % (task, taskData.fn_index[taskData.tasks_fnid[task]], taskData.tasks_name[task], depends))
                    for dep in depends:
                        if task != dep:
                            newdep.append(dep)
                    depends = newdep

            self.runq_fnid.append(taskData.tasks_fnid[task])
            self.runq_task.append(taskData.tasks_name[task])
            self.runq_depends.append(set(depends))
            self.runq_revdeps.append(set())
            self.runq_hash.append("")

            runq_build.append(0)
            runq_recrdepends.append(recrdepends)

        #
        # Build a list of recursive cumulative dependencies for each fnid
        # We do this by fnid, since if A depends on some task in B
        # we're interested in later tasks B's fnid might have but B itself
        # doesn't depend on
        #
        # Algorithm is O(tasks) + O(tasks)*O(fnids)
        #
        reccumdepends = {}
        for task in range(len(self.runq_fnid)):
            fnid = self.runq_fnid[task]
            if fnid not in reccumdepends:
                if fnid in tdepends_fnid:
                    reccumdepends[fnid] = tdepends_fnid[fnid]
                else:
                    reccumdepends[fnid] = set()
            reccumdepends[fnid].update(self.runq_depends[task])
        for task in range(len(self.runq_fnid)):
            taskfnid = self.runq_fnid[task]
            for fnid in reccumdepends:
                if task in reccumdepends[fnid]:
                    reccumdepends[fnid].add(task)
                    if taskfnid in reccumdepends:
                        reccumdepends[fnid].update(reccumdepends[taskfnid])


        # Resolve recursive 'recrdeptask' dependencies (B)
        #
        # e.g. do_sometask[recrdeptask] = "do_someothertask"
        # (makes sure sometask runs after someothertask of all DEPENDS, RDEPENDS and intertask dependencies, recursively)
        for task in range(len(self.runq_fnid)):
            if len(runq_recrdepends[task]) > 0:
                taskfnid = self.runq_fnid[task]
                for dep in reccumdepends[taskfnid]:
                    # Ignore self references
                    if dep == task:
                        continue
                    for taskname in runq_recrdepends[task]:
                        if taskData.tasks_name[dep] == taskname:
                            self.runq_depends[task].add(dep)

        # Step B - Mark all active tasks
        #
        # Start with the tasks we were asked to run and mark all dependencies
        # as active too. If the task is to be 'forced', clear its stamp. Once
        # all active tasks are marked, prune the ones we don't need.

        bb.msg.note(2, bb.msg.domain.RunQueue, "Marking Active Tasks")

        def mark_active(listid, depth):
            """
            Mark an item as active along with its depends
            (calls itself recursively)
            """

            if runq_build[listid] == 1:
                return

            runq_build[listid] = 1

            depends = self.runq_depends[listid]
            for depend in depends:
                mark_active(depend, depth+1)

        self.target_pairs = []
        for target in self.targets:
            targetid = taskData.getbuild_id(target[0])

            if targetid not in taskData.build_targets:
                continue

            if targetid in taskData.failed_deps:
                continue

            fnid = taskData.build_targets[targetid][0]
            fn = taskData.fn_index[fnid]
            self.target_pairs.append((fn, target[1]))

            # Remove stamps for targets if force mode active
            if self.cooker.configuration.force:
                bb.msg.note(2, bb.msg.domain.RunQueue, "Remove stamp %s, %s" % (target[1], fn))
                bb.build.del_stamp(target[1], self.dataCache, fn)

            if fnid in taskData.failed_fnids:
                continue

            if target[1] not in taskData.tasks_lookup[fnid]:
                bb.msg.fatal(bb.msg.domain.RunQueue, "Task %s does not exist for target %s" % (target[1], target[0]))

            listid = taskData.tasks_lookup[fnid][target[1]]

            mark_active(listid, 1)

        # Step C - Prune all inactive tasks
        #
        # Once all active tasks are marked, prune the ones we don't need.

        maps = []
        delcount = 0
        for listid in range(len(self.runq_fnid)):
            if runq_build[listid-delcount] == 1:
                maps.append(listid-delcount)
            else:
                del self.runq_fnid[listid-delcount]
                del self.runq_task[listid-delcount]
                del self.runq_depends[listid-delcount]
                del runq_build[listid-delcount]
                del self.runq_revdeps[listid-delcount]
                del self.runq_hash[listid-delcount]
                delcount = delcount + 1
                maps.append(-1)

        #
        # Step D - Sanity checks and computation
        #

        # Check to make sure we still have tasks to run
        if len(self.runq_fnid) == 0:
            if not taskData.abort:
                bb.msg.fatal(bb.msg.domain.RunQueue, "All buildable tasks have been run but the build is incomplete (--continue mode). Errors for the tasks that failed will have been printed above.")
            else:
                bb.msg.fatal(bb.msg.domain.RunQueue, "No active tasks and not in --continue mode?! Please report this bug.")

        bb.msg.note(2, bb.msg.domain.RunQueue, "Pruned %s inactive tasks, %s left" % (delcount, len(self.runq_fnid)))

        # Remap the dependencies to account for the deleted tasks
        # Check we didn't delete a task we depend on
        for listid in range(len(self.runq_fnid)):
            newdeps = []
            origdeps = self.runq_depends[listid]
            for origdep in origdeps:
                if maps[origdep] == -1:
                    bb.msg.fatal(bb.msg.domain.RunQueue, "Invalid mapping - Should never happen!")
                newdeps.append(maps[origdep])
            self.runq_depends[listid] = set(newdeps)

        bb.msg.note(2, bb.msg.domain.RunQueue, "Assign Weightings")

        # Generate a list of reverse dependencies to ease future calculations
        for listid in range(len(self.runq_fnid)):
            for dep in self.runq_depends[listid]:
                self.runq_revdeps[dep].add(listid)

        # Identify tasks at the end of dependency chains
        # Error on circular dependency loops (length two)
        endpoints = []
        for listid in range(len(self.runq_fnid)):
            revdeps = self.runq_revdeps[listid]
            if len(revdeps) == 0:
                endpoints.append(listid)
            for dep in revdeps:
                if dep in self.runq_depends[listid]:
                    #self.dump_data(taskData)
                    bb.msg.fatal(bb.msg.domain.RunQueue, "Task %s (%s) has circular dependency on %s (%s)" % (taskData.fn_index[self.runq_fnid[dep]], self.runq_task[dep], taskData.fn_index[self.runq_fnid[listid]], self.runq_task[listid]))

        bb.msg.note(2, bb.msg.domain.RunQueue, "Compute totals (have %s endpoint(s))" % len(endpoints))

        # Calculate task weights
        # Check of higher length circular dependencies
        self.runq_weight = self.calculate_task_weights(endpoints)

        # Sanity Check - Check for multiple tasks building the same provider
        prov_list = {}
        seen_fn = []
        for task in range(len(self.runq_fnid)):
            fn = taskData.fn_index[self.runq_fnid[task]]
            if fn in seen_fn:
                continue
            seen_fn.append(fn)
            for prov in self.dataCache.fn_provides[fn]:
                if prov not in prov_list:
                    prov_list[prov] = [fn]
                elif fn not in prov_list[prov]:
                    prov_list[prov].append(fn)
        error = False
        for prov in prov_list:
            if len(prov_list[prov]) > 1 and prov not in self.multi_provider_whitelist:
                error = True
                bb.msg.error(bb.msg.domain.RunQueue, "Multiple .bb files are due to be built which each provide %s (%s).\n This usually means one provides something the other doesn't and should." % (prov, " ".join(prov_list[prov])))
        #if error:
        #    bb.msg.fatal(bb.msg.domain.RunQueue, "Corrupted metadata configuration detected, aborting...")


        # Create a whitelist usable by the stamp checks
        stampfnwhitelist = []
        for entry in self.stampwhitelist.split():
            entryid = self.taskData.getbuild_id(entry)
            if entryid not in self.taskData.build_targets:
                continue
            fnid = self.taskData.build_targets[entryid][0]
            fn = self.taskData.fn_index[fnid]
            stampfnwhitelist.append(fn)
        self.stampfnwhitelist = stampfnwhitelist

        #self.dump_data(taskData)

        # Interate over the task list looking for tasks with a 'setscene' function

        self.runq_setscene = []
        for task in range(len(self.runq_fnid)):
            setscene = taskData.gettask_id(self.taskData.fn_index[self.runq_fnid[task]], self.runq_task[task] + "_setscene", False)
            if not setscene:
                continue
            #bb.note("Found setscene for %s %s" % (self.taskData.fn_index[self.runq_fnid[task]], self.runq_task[task]))
            self.runq_setscene.append(task)

        # Interate over the task list and call into the siggen code

        dealtwith = set()
        todeal = set(range(len(self.runq_fnid)))
        while len(todeal) > 0:
            for task in todeal.copy():
                if len(self.runq_depends[task] - dealtwith) == 0:
                    dealtwith.add(task)
                    todeal.remove(task)
                    procdep = []
                    for dep in self.runq_depends[task]:
                        procdep.append(self.taskData.fn_index[self.runq_fnid[dep]] + "." + self.runq_task[dep])
                    self.runq_hash[task] = bb.parse.siggen.get_taskhash(self.taskData.fn_index[self.runq_fnid[task]], self.runq_task[task], procdep, self.dataCache)

        hashdata = {}
        hashdata["hashes"] = {}
        hashdata["deps"] = {}
        for task in range(len(self.runq_fnid)):
            hashdata["hashes"][self.taskData.fn_index[self.runq_fnid[task]] + "." + self.runq_task[task]] = self.runq_hash[task]
            deps = []
            for dep in self.runq_depends[task]:
                deps.append(self.taskData.fn_index[self.runq_fnid[dep]] + "." + self.runq_task[dep])
            hashdata["deps"][self.taskData.fn_index[self.runq_fnid[task]] + "." + self.runq_task[task]] = deps

        hashdata["msg-debug"] = self.cooker.configuration.debug
        hashdata["msg-debug-domains"] =  self.cooker.configuration.debug_domains
        hashdata["verbose"] = self.cooker.configuration.verbose

        # Write out the hashes into a file for use by the individual tasks
        self.hashfile = bb.data.expand("${TMPDIR}/cache/hashdata.dat", self.cooker.configuration.data)
        p = pickle.Pickler(file(self.hashfile, "wb"), -1)
        p.dump(hashdata)

        return len(self.runq_fnid)

    def dump_data(self, taskQueue):
        """
        Dump some debug information on the internal data structures
        """
        bb.msg.debug(3, bb.msg.domain.RunQueue, "run_tasks:")
        for task in range(len(self.rqdata.runq_task)):
            bb.msg.debug(3, bb.msg.domain.RunQueue, " (%s)%s - %s: %s   Deps %s RevDeps %s" % (task,
                taskQueue.fn_index[self.rqdata.runq_fnid[task]],
                self.rqdata.runq_task[task],
                self.rqdata.runq_weight[task],
                self.rqdata.runq_depends[task],
                self.rqdata.runq_revdeps[task]))

        bb.msg.debug(3, bb.msg.domain.RunQueue, "sorted_tasks:")
        for task1 in range(len(self.rqdata.runq_task)):
            if task1 in self.prio_map:
                task = self.prio_map[task1]
                bb.msg.debug(3, bb.msg.domain.RunQueue, " (%s)%s - %s: %s   Deps %s RevDeps %s" % (task,
                    taskQueue.fn_index[self.rqdata.runq_fnid[task]],
                    self.rqdata.runq_task[task],
                    self.rqdata.runq_weight[task],
                    self.rqdata.runq_depends[task],
                    self.rqdata.runq_revdeps[task]))

class RunQueue:
    def __init__(self, cooker, cfgData, dataCache, taskData, targets):

        self.cooker = cooker
        self.cfgData = cfgData
        self.rqdata = RunQueueData(self, cooker, cfgData, dataCache, taskData, targets)

        self.stamppolicy = bb.data.getVar("BB_STAMP_POLICY", cfgData, True) or "perfile"
        self.hashvalidate = bb.data.getVar("BB_HASHCHECK_FUNCTION", cfgData, True) or None

        self.state = runQueuePrepare

    def check_stamps(self):
        unchecked = {}
        current = []
        notcurrent = []
        buildable = []

        if self.stamppolicy == "perfile":
            fulldeptree = False
        else:
            fulldeptree = True
            stampwhitelist = []
            if self.stamppolicy == "whitelist":
                stampwhitelist = self.rqdata.stampfnwhitelist

        for task in range(len(self.rqdata.runq_fnid)):
            unchecked[task] = ""
            if len(self.rqdata.runq_depends[task]) == 0:
                buildable.append(task)

        def check_buildable(self, task, buildable):
            for revdep in self.rqdata.runq_revdeps[task]:
                alldeps = 1
                for dep in self.rqdata.runq_depends[revdep]:
                    if dep in unchecked:
                        alldeps = 0
                if alldeps == 1:
                    if revdep in unchecked:
                        buildable.append(revdep)

        for task in range(len(self.rqdata.runq_fnid)):
            if task not in unchecked:
                continue
            fn = self.rqdata.taskData.fn_index[self.rqdata.runq_fnid[task]]
            taskname = self.rqdata.runq_task[task]
            stampfile = "%s.%s" % (self.rqdata.dataCache.stamp[fn], taskname)
            # If the stamp is missing its not current
            if not os.access(stampfile, os.F_OK):
                del unchecked[task]
                notcurrent.append(task)
                check_buildable(self, task, buildable)
                continue
            # If its a 'nostamp' task, it's not current
            taskdep = self.rqdata.dataCache.task_deps[fn]
            if 'nostamp' in taskdep and task in taskdep['nostamp']:
                del unchecked[task]
                notcurrent.append(task)
                check_buildable(self, task, buildable)
                continue

        while (len(buildable) > 0):
            nextbuildable = []
            for task in buildable:
                if task in unchecked:
                    fn = self.taskData.fn_index[self.rqdata.runq_fnid[task]]
                    taskname = self.rqdata.runq_task[task]
                    stampfile = "%s.%s" % (self.rqdata.dataCache.stamp[fn], taskname)
                    iscurrent = True

                    t1 = os.stat(stampfile)[stat.ST_MTIME]
                    for dep in self.rqdata.runq_depends[task]:
                        if iscurrent:
                            fn2 = self.taskData.fn_index[self.rqdata.runq_fnid[dep]]
                            taskname2 = self.rqdata.runq_task[dep]
                            stampfile2 = "%s.%s" % (self.rqdata.dataCache.stamp[fn2], taskname2)
                            if fn == fn2 or (fulldeptree and fn2 not in stampwhitelist):
                                if dep in notcurrent:
                                    iscurrent = False
                                else:
                                    t2 = os.stat(stampfile2)[stat.ST_MTIME]
                                    if t1 < t2:
                                        iscurrent = False
                    del unchecked[task]
                    if iscurrent:
                        current.append(task)
                    else:
                        notcurrent.append(task)

                check_buildable(self, task, nextbuildable)

            buildable = nextbuildable

        #for task in range(len(self.runq_fnid)):
        #    fn = self.taskData.fn_index[self.runq_fnid[task]]
        #    taskname = self.runq_task[task]
        #    print "%s %s.%s" % (task, taskname, fn)

        #print "Unchecked: %s" % unchecked
        #print "Current: %s" % current
        #print "Not current: %s" % notcurrent

        if len(unchecked) > 0:
            bb.msg.fatal(bb.msg.domain.RunQueue, "check_stamps fatal internal error")
        return current

    def check_stamp_task(self, task, taskname = None):
        def get_timestamp(f):
            try:
                if not os.access(f, os.F_OK):
                    return None
                return os.stat(f)[stat.ST_MTIME]
            except:
                return None

        if self.stamppolicy == "perfile":
            fulldeptree = False
        else:
            fulldeptree = True
            stampwhitelist = []
            if self.stamppolicy == "whitelist":
                stampwhitelist = self.rqdata.stampfnwhitelist

        fn = self.rqdata.taskData.fn_index[self.rqdata.runq_fnid[task]]
        if taskname is None:
            taskname = self.rqdata.runq_task[task]
        
        stampfile = bb.parse.siggen.stampfile(self.rqdata.dataCache.stamp[fn], taskname, self.rqdata.runq_hash[task])

        # If the stamp is missing its not current
        if not os.access(stampfile, os.F_OK):
            bb.msg.debug(2, bb.msg.domain.RunQueue, "Stampfile %s not available\n" % stampfile)
            return False
        # If its a 'nostamp' task, it's not current
        taskdep = self.rqdata.dataCache.task_deps[fn]
        if 'nostamp' in taskdep and taskname in taskdep['nostamp']:
            bb.msg.debug(2, bb.msg.domain.RunQueue, "%s.%s is nostamp\n" % (fn, taskname))
            return False

        if taskname.endswith("_setscene"):
            return True

        iscurrent = True
        t1 = get_timestamp(stampfile)
        for dep in self.rqdata.runq_depends[task]:
            if iscurrent:
                fn2 = self.rqdata.taskData.fn_index[self.rqdata.runq_fnid[dep]]
                taskname2 = self.rqdata.runq_task[dep]
                stampfile2 = bb.parse.siggen.stampfile(self.rqdata.dataCache.stamp[fn2], taskname2, self.rqdata.runq_hash[dep])
                stampfile3 = bb.parse.siggen.stampfile(self.rqdata.dataCache.stamp[fn2], taskname2 + "_setscene", self.rqdata.runq_hash[dep])
                t2 = get_timestamp(stampfile2)
                t3 = get_timestamp(stampfile3)
                if t3 and t3 > t2:
                   continue
                if fn == fn2 or (fulldeptree and fn2 not in stampwhitelist):
                    if not t2 or t1 < t2:
                        bb.msg.debug(2, bb.msg.domain.RunQueue, "Stampfile %s < %s (or does not exist)" % (stampfile, stampfile2))
                        iscurrent = False
        return iscurrent

    def execute_runqueue(self):
        """
        Run the tasks in a queue prepared by rqdata.prepare()
        Upon failure, optionally try to recover the build using any alternate providers
        (if the abort on failure configuration option isn't set)
        """

        retval = 0.5

        if self.state is runQueuePrepare:
            self.rqexe = RunQueueExecuteDummy(self)
            if self.rqdata.prepare() is 0:
                self.state = runQueueComplete
            else:
                self.state = runQueueSceneInit

        if self.state is runQueueSceneInit:
            if self.cooker.configuration.dump_signatures:
                self.dump_signatures()
            else:
                self.rqexe = RunQueueExecuteScenequeue(self)

        if self.state is runQueueSceneRun:
            retval = self.rqexe.execute()

        if self.state is runQueueRunInit:
            bb.msg.note(1, bb.msg.domain.RunQueue, "Executing runqueue")
            self.rqexe = RunQueueExecuteTasks(self)
            self.state = runQueueRunning

        if self.state is runQueueRunning:
            retval = self.rqexe.execute()

        if self.state is runQueueCleanUp:
           self.rqexe.finish()

        if self.state is runQueueFailed:
            if not self.rqdata.taskData.tryaltconfigs:
                raise bb.runqueue.TaskFailure(self.rqexe.failed_fnids)
            for fnid in self.rqexe.failed_fnids:
                self.rqdata.taskData.fail_fnid(fnid)
            self.rqdata.reset()

        if self.state is runQueueComplete:
            # All done
            bb.msg.note(1, bb.msg.domain.RunQueue, "Tasks Summary: Attempted %d tasks of which %d didn't need to be rerun and %d failed." % (self.rqexe.stats.completed, self.rqexe.stats.skipped, self.rqexe.stats.failed))
            return False

        if self.state is runQueueChildProcess:
            print("Child process, eeek, shouldn't happen!")
            return False

        # Loop
        return retval

    def finish_runqueue(self, now = False):
        if now:
            self.rqexe.finish_now()
        else:
            self.rqexe.finish()

    def dump_signatures(self):
        self.state = runQueueComplete
        done = set()
        bb.note("Reparsing files to collect dependency data")
        for task in range(len(self.rqdata.runq_fnid)):
            if self.rqdata.runq_fnid[task] not in done:
                fn = self.rqdata.taskData.fn_index[self.rqdata.runq_fnid[task]] 
                the_data = self.cooker.bb_cache.loadDataFull(fn, self.cooker.get_file_appends(fn), self.cooker.configuration.data)
                done.add(self.rqdata.runq_fnid[task])

        bb.parse.siggen.dump_sigs(self.rqdata.dataCache)

        return


class RunQueueExecute:

    def __init__(self, rq):
        self.rq = rq
        self.cooker = rq.cooker
        self.cfgData = rq.cfgData
        self.rqdata = rq.rqdata

        self.number_tasks = int(bb.data.getVar("BB_NUMBER_THREADS", self.cfgData, 1) or 1)
        self.scheduler = bb.data.getVar("BB_SCHEDULER", self.cfgData, 1) or "speed"

        self.runq_buildable = []
        self.runq_running = []
        self.runq_complete = []
        self.build_pids = {}
        self.build_pipes = {}
        self.build_procs = {}
        self.build_sockpids = {}
        self.build_sockfiles = {}
        self.failed_fnids = []

    def runqueue_process_waitpid(self):
        """
        Return none is there are no processes awaiting result collection, otherwise
        collect the process exit codes and close the information pipe.
        """
        for pid in self.build_procs.keys():
            proc = self.build_procs[pid]
            proc.poll()
            if proc.returncode is not None:
                task = self.build_pids[pid]
                sockfile = self.build_sockfiles[pid]
                sockpid = self.build_sockpids[pid]
                os.waitpid(sockpid, 0)
                os.unlink(sockfile)
                del self.build_pids[pid]
                self.build_pipes[pid].close()
                del self.build_pipes[pid]
                del self.build_procs[pid]
                del self.build_sockpids[pid]
                del self.build_sockfiles[pid]
                if proc.returncode != 0:
                    self.task_fail(task, proc.returncode)
                else:
                    self.task_complete(task)

    def finish_now(self):
        if self.stats.active:
            bb.msg.note(1, bb.msg.domain.RunQueue, "Sending SIGINT to remaining %s tasks" % self.stats.active)
            for k, v in self.build_pids.iteritems():
                try:
                    os.kill(-k, signal.SIGINT)
                except:
                    pass
        for pipe in self.build_pipes:
            self.build_pipes[pipe].read()

    def finish(self):
        self.rq.state = runQueueCleanUp

        for pipe in self.build_pipes:
            self.build_pipes[pipe].read()

        if self.stats.active > 0:
            bb.event.fire(runQueueExitWait(self.stats.active), self.cfgData)
            self.runqueue_process_waitpid()
            return

        if len(self.failed_fnids) != 0:
            self.rq.state = runQueueFailed
            return

        self.rq.state = runQueueComplete
        return

    def fork_off_task(self, fn, task, taskname):
        the_data = self.cooker.bb_cache.loadDataFull(fn, self.cooker.get_file_appends(fn), self.cooker.configuration.data)

        sockfile = os.tempnam("/tmp", "sock-")
        sockpid = os.fork()
        if sockpid == 0:
            import socket

            try:
                #si = file("/dev/null", 'r')
                #os.dup2(si.fileno( ), sys.stdin.fileno( ))
                #so = file("/dev/null", 'w')
                #os.dup2(so.fileno( ), sys.stdout.fileno( ))
                #os.dup2(so.fileno( ), sys.stderr.fileno( ))

                os.setpgrp()
                signal.signal(signal.SIGPIPE, signal.SIG_DFL)
                signal.signal(signal.SIGINT, signal.SIG_DFL)

                bb.event.worker_pid = 0

                s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                s.bind(sockfile)
                s.listen(1)
                conn, _ = s.accept()

                while 1:
                    k = conn.recv(1024)
                    if k == "_cmd_end":
                        conn.flush()
                        conn.close()
                        os._exit(os.EX_OK)
                    elif k == "_cmd_parsed_fns":
                        dump = pickle.dumps(bb.methodpool.get_parsed_fns())
                    elif k == "_cmd_keys":
                        dump = pickle.dumps(the_data.keys())
                    else:
                        dump = pickle.dumps(the_data._findVar(k))

                    conn.send("%04x" % len(dump))
                    conn.sendall(dump)
            except:
                pass
            os._exit(os.EX_OK)

        try:
            env = bb.data.export_vars(the_data)
            env = bb.data.export_envvars(env, the_data)

            taskdep = self.rqdata.dataCache.task_deps[fn]
            if 'fakeroot' in taskdep and taskname in taskdep['fakeroot']:
                envvars = the_data.getVar("FAKEROOTENV", True).split()
                for var in envvars:
                    comps = var.split("=")
                    env[comps[0]] = comps[1]
                fakedirs = (the_data.getVar("FAKEROOTDIRS", True) or "").split()
                for p in fakedirs:
                    bb.mkdirhier(p)
                bb.msg.debug(2, bb.msg.domain.RunQueue, "Running %s:%s under fakeroot, state dir is %s" % (fn, taskname, fakedirs))

            env['BB_TASKHASH'] = self.rqdata.runq_hash[task]
            env['PATH'] = self.cooker.configuration.initial_path

            sys.stdout.flush()
            sys.stderr.flush()

            runtask = the_data.getVar("BB_RUNTASK", True) or "bitbake-runtask"
            proc = subprocess.Popen([runtask, self.rqdata.hashfile, fn, taskname, str(self.cooker.configuration.dry_run), sockfile], env=env, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            pipein = proc.stdout
            pipeout = proc.stdin
            pid = proc.pid
        except OSError as e: 
            bb.msg.fatal(bb.msg.domain.RunQueue, "fork failed: %d (%s)" % (e.errno, e.strerror))

        return proc, sockpid, sockfile

class RunQueueExecuteDummy(RunQueueExecute):
    def __init__(self, rq):
        self.rq = rq
        self.stats = RunQueueStats(0)
    def finish(self):
        self.rq.state = runQueueComplete
        return    

class RunQueueExecuteTasks(RunQueueExecute):
    def __init__(self, rq):
        RunQueueExecute.__init__(self, rq)

        self.stats = RunQueueStats(len(self.rqdata.runq_fnid))

        # Mark initial buildable tasks
        for task in range(self.stats.total):
            self.runq_running.append(0)
            self.runq_complete.append(0)
            if len(self.rqdata.runq_depends[task]) == 0:
                self.runq_buildable.append(1)
            else:
                self.runq_buildable.append(0)
            if len(self.rqdata.runq_revdeps[task]) > 0 and self.rqdata.runq_revdeps[task].issubset(self.rq.scenequeue_covered):
                self.rq.scenequeue_covered.add(task)

        found = True
        while found:
            found = False
            for task in range(self.stats.total):
                if task in self.rq.scenequeue_covered:
                    continue
                if len(self.rqdata.runq_revdeps[task]) > 0 and self.rqdata.runq_revdeps[task].issubset(self.rq.scenequeue_covered):
                    self.rq.scenequeue_covered.add(task)
                    found = True

        bb.note("Full skip list %s" % self.rq.scenequeue_covered)

        for task in self.rq.scenequeue_covered:
            self.task_skip(task)

        event.fire(bb.event.StampUpdate(self.rqdata.target_pairs, self.rqdata.dataCache.stamp), self.cfgData)

        schedulers = [obj for obj in globals().itervalues()
                      if type(obj) is type and issubclass(obj, RunQueueScheduler)]
        for scheduler in schedulers:
            if self.scheduler == scheduler.name:
                self.sched = scheduler(self, self.rqdata)
                break
        else:
            bb.error("Invalid scheduler '%s', using default 'speed' scheduler" % self.scheduler)
            bb.error("Available schedulers: %s" % ", ".join(obj.name for obj in schedulers))
            self.sched = RunQueueSchedulerSpeed(self, self.rqdata)


    def task_completeoutright(self, task):
        """
        Mark a task as completed
        Look at the reverse dependencies and mark any task with
        completed dependencies as buildable
        """
        self.runq_complete[task] = 1
        for revdep in self.rqdata.runq_revdeps[task]:
            if self.runq_running[revdep] == 1:
                continue
            if self.runq_buildable[revdep] == 1:
                continue
            alldeps = 1
            for dep in self.rqdata.runq_depends[revdep]:
                if self.runq_complete[dep] != 1:
                    alldeps = 0
            if alldeps == 1:
                self.runq_buildable[revdep] = 1
                fn = self.rqdata.taskData.fn_index[self.rqdata.runq_fnid[revdep]]
                taskname = self.rqdata.runq_task[revdep]
                bb.msg.debug(1, bb.msg.domain.RunQueue, "Marking task %s (%s, %s) as buildable" % (revdep, fn, taskname))

    def task_complete(self, task):
        self.stats.taskCompleted()
        bb.event.fire(runQueueTaskCompleted(task, self.stats, self.rq), self.cfgData)
        self.task_completeoutright(task)

    def task_fail(self, task, exitcode):
        """
        Called when a task has failed
        Updates the state engine with the failure
        """
        bb.msg.error(bb.msg.domain.RunQueue, "Task %s (%s) failed with %s" % (task, self.rqdata.get_user_idstring(task), exitcode))
        self.stats.taskFailed()
        fnid = self.rqdata.runq_fnid[task]
        self.failed_fnids.append(fnid)
        bb.event.fire(runQueueTaskFailed(task, self.stats, self.rq), self.cfgData)
        if self.rqdata.taskData.abort:
            self.rq.state = runQueueCleanUp

    def task_skip(self, task):
        self.runq_running[task] = 1
        self.runq_buildable[task] = 1
        self.task_completeoutright(task)
        self.stats.taskCompleted()
        self.stats.taskSkipped()

    def execute(self):
        """
        Run the tasks in a queue prepared by rqdata.prepare()
        """

        if self.stats.total == 0:
            # nothing to do
            self.rq.state = runQueueCleanUp

        task = None
        if self.stats.active < self.number_tasks:
            task = self.sched.next()
        if task is not None:
            fn = self.rqdata.taskData.fn_index[self.rqdata.runq_fnid[task]]

            taskname = self.rqdata.runq_task[task]
            if self.rq.check_stamp_task(task, taskname):
                bb.msg.debug(2, bb.msg.domain.RunQueue, "Stamp current task %s (%s)" % (task, self.rqdata.get_user_idstring(task)))
                self.task_skip(task)
                return True

            bb.event.fire(runQueueTaskStarted(task, self.stats, self.rq), self.cfgData)

            taskdep = self.rqdata.dataCache.task_deps[fn]
            if 'noexec' in taskdep and taskname in taskdep['noexec']:
                bb.msg.note(1, bb.msg.domain.RunQueue,
                        "Noexec task %d of %d (ID: %s, %s)" % (self.stats.completed + self.stats.active + self.stats.failed + 1,
                                                                self.stats.total,
                                                                task,
                                                                self.rqdata.get_user_idstring(task)))
                self.runq_running[task] = 1
                self.stats.taskActive()
                bb.build.make_stamp(taskname, self.rqdata.dataCache, fn)
                self.task_complete(task)
                return True

            bb.msg.note(1, bb.msg.domain.RunQueue,
                        "Running task %d of %d (ID: %s, %s)" % (self.stats.completed + self.stats.active + self.stats.failed + 1,
                                                                self.stats.total,
                                                                task,
                                                                self.rqdata.get_user_idstring(task)))

            proc, sockpid, sockfile = self.fork_off_task(fn, task, taskname)

            self.build_pids[proc.pid] = task
            self.build_procs[proc.pid] = proc
            self.build_pipes[proc.pid] = runQueuePipe(proc.stdout, proc.stdin, self.cfgData)
            self.build_sockpids[proc.pid] = sockpid
            self.build_sockfiles[proc.pid] = sockfile
            self.runq_running[task] = 1
            self.stats.taskActive()
            if self.stats.active < self.number_tasks:
                return True

        for pipe in self.build_pipes:
            self.build_pipes[pipe].read()

        if self.stats.active > 0:
            if self.runqueue_process_waitpid() is None:
                return 0.5
            return True

        if len(self.failed_fnids) != 0:
            self.rq.state = runQueueFailed
            return True

        # Sanity Checks
        for task in range(self.stats.total):
            if self.runq_buildable[task] == 0:
                bb.msg.error(bb.msg.domain.RunQueue, "Task %s never buildable!" % task)
            if self.runq_running[task] == 0:
                bb.msg.error(bb.msg.domain.RunQueue, "Task %s never ran!" % task)
            if self.runq_complete[task] == 0:
                bb.msg.error(bb.msg.domain.RunQueue, "Task %s never completed!" % task)
        self.rq.state = runQueueComplete
        return True

class RunQueueExecuteScenequeue(RunQueueExecute):
    def __init__(self, rq):
        RunQueueExecute.__init__(self, rq)

        self.scenequeue_covered = set()
        self.scenequeue_notcovered = set()

        # If we don't have any setscene functions, skip this step
        if len(self.rqdata.runq_setscene) == 0:
            rq.scenequeue_covered = set()
            rq.state = runQueueRunInit
            return

        self.stats = RunQueueStats(len(self.rqdata.runq_setscene))

        endpoints = {}
        sq_revdeps = []
        sq_revdeps_new = []
        sq_revdeps_squash = []

        # We need to construct a dependency graph for the setscene functions. Intermediate
        # dependencies between the setscene tasks only complicate the code. This code
        # therefore aims to collapse the huge runqueue dependency tree into a smaller one
        # only containing the setscene functions.

        for task in range(self.stats.total):
            self.runq_running.append(0)
            self.runq_complete.append(0)
            self.runq_buildable.append(0)

        for task in range(len(self.rqdata.runq_fnid)):
            sq_revdeps.append(copy.copy(self.rqdata.runq_revdeps[task]))
            sq_revdeps_new.append(set())
            if (len(self.rqdata.runq_revdeps[task]) == 0) and task not in self.rqdata.runq_setscene:
                endpoints[task] = None

        for task in self.rqdata.runq_setscene:
            for dep in self.rqdata.runq_depends[task]:
                    endpoints[dep] = task

        def process_endpoints(endpoints):
            newendpoints = {}
            for point, task in endpoints.items():
                tasks = set()
                if task:
                    tasks.add(task)
                if sq_revdeps_new[point]:
                    tasks |= sq_revdeps_new[point]
                sq_revdeps_new[point] = set()
                for dep in self.rqdata.runq_depends[point]:
                    if point in sq_revdeps[dep]:
                        sq_revdeps[dep].remove(point)
                    if tasks:
                        sq_revdeps_new[dep] |= tasks
                    if (len(sq_revdeps[dep]) == 0 or len(sq_revdeps_new[dep]) != 0) and dep not in self.rqdata.runq_setscene:
                        newendpoints[dep] = task
            if len(newendpoints) != 0:
                process_endpoints(newendpoints)

        process_endpoints(endpoints)

        for task in range(len(self.rqdata.runq_fnid)):
            if task in self.rqdata.runq_setscene:
                deps = set()
                for dep in sq_revdeps_new[task]:
                    deps.add(self.rqdata.runq_setscene.index(dep))
                sq_revdeps_squash.append(deps)
            elif len(sq_revdeps_new[task]) != 0:
                bb.msg.fatal(bb.msg.domain.RunQueue, "Something went badly wrong during scenequeue generation, aborting. Please report this problem.")

        #for task in range(len(sq_revdeps_squash)):
        #    print "Task %s: %s.%s is %s " % (task, self.taskData.fn_index[self.runq_fnid[self.runq_setscene[task]]], self.runq_task[self.runq_setscene[task]] + "_setscene", sq_revdeps_squash[task])

        self.sq_deps = []
        self.sq_revdeps = sq_revdeps_squash
        self.sq_revdeps2 = copy.deepcopy(self.sq_revdeps)

        for task in range(len(self.sq_revdeps)):
            self.sq_deps.append(set())
        for task in range(len(self.sq_revdeps)):
            for dep in self.sq_revdeps[task]:
                self.sq_deps[dep].add(task)

        for task in range(len(self.sq_revdeps)):
            if len(self.sq_revdeps[task]) == 0:
                self.runq_buildable[task] = 1

        if self.rq.hashvalidate:
            sq_hash = []
            sq_hashfn = []
            sq_fn = []
            sq_task = []
            noexec = []
            for task in range(len(self.sq_revdeps)):
                realtask = self.rqdata.runq_setscene[task]
                fn = self.rqdata.taskData.fn_index[self.rqdata.runq_fnid[realtask]]
                taskname = self.rqdata.runq_task[realtask]
                taskdep = self.rqdata.dataCache.task_deps[fn]
                if 'noexec' in taskdep and taskname in taskdep['noexec']:
                    noexec.append(task)
                    self.task_skip(task)
                    continue
                sq_fn.append(fn)
                sq_hashfn.append(self.rqdata.dataCache.hashfn[fn])
                sq_hash.append(self.rqdata.runq_hash[realtask])
                sq_task.append(taskname)

            call = self.rq.hashvalidate + "(sq_fn, sq_task, sq_hash, sq_hashfn, d)"
            locs = { "sq_fn" : sq_fn, "sq_task" : sq_task, "sq_hash" : sq_hash, "sq_hashfn" : sq_hashfn, "d" : self.cooker.configuration.data }
            valid = bb.utils.better_eval(call, locs)
            for task in range(len(self.sq_revdeps)):
                if task not in valid and task not in noexec:
                    bb.msg.debug(2, bb.msg.domain.RunQueue, "No package found so skipping setscene task %s" % (self.rqdata.get_user_idstring(task)))
                    self.task_failoutright(task)

            #print(str(valid))

        bb.msg.note(1, bb.msg.domain.RunQueue, "Executing setscene Tasks")

        self.rq.state = runQueueSceneRun

    def scenequeue_updatecounters(self, task):
        for dep in self.sq_deps[task]:
            self.sq_revdeps2[dep].remove(task)
            if len(self.sq_revdeps2[dep]) == 0:
                self.runq_buildable[dep] = 1

    def task_completeoutright(self, task):
        """
        Mark a task as completed
        Look at the reverse dependencies and mark any task with
        completed dependencies as buildable
        """

        index = self.rqdata.runq_setscene[task]
        bb.msg.note(1, bb.msg.domain.RunQueue, "Found task %s could be accelerated" % self.rqdata.get_user_idstring(index))

        self.scenequeue_covered.add(task)
        self.scenequeue_updatecounters(task)

    def task_complete(self, task):
        self.stats.taskCompleted()
        self.task_completeoutright(task)

    def task_fail(self, task, result):
        self.stats.taskFailed()
        index = self.rqdata.runq_setscene[task]
        bb.event.fire(runQueueTaskFailed(task, self.stats, self), self.cfgData)
        self.scenequeue_notcovered.add(task)
        self.scenequeue_updatecounters(task)

    def task_failoutright(self, task):
        self.runq_running[task] = 1
        self.runq_buildable[task] = 1
        self.stats.taskCompleted()
        self.stats.taskSkipped()
        index = self.rqdata.runq_setscene[task]
        self.scenequeue_notcovered.add(task)
        self.scenequeue_updatecounters(task)

    def task_skip(self, task):
        self.runq_running[task] = 1
        self.runq_buildable[task] = 1
        self.task_completeoutright(task)
        self.stats.taskCompleted()
        self.stats.taskSkipped()

    def execute(self):
        """
        Run the tasks in a queue prepared by prepare_runqueue
        """

        task = None
        if self.stats.active < self.number_tasks:
            # Find the next setscene to run
            for nexttask in range(self.stats.total):
                if self.runq_buildable[nexttask] == 1 and self.runq_running[nexttask] != 1:
                    #bb.note("Comparing %s to %s" % (self.sq_revdeps[nexttask], self.scenequeue_covered))
                    #if len(self.sq_revdeps[nexttask]) > 0 and self.sq_revdeps[nexttask].issubset(self.scenequeue_covered):
                    #    bb.note("Skipping task %s" % nexttask)
                    #    self.scenequeue_skip(nexttask)
                    #    return True
                    task = nexttask
                    break
        if task is not None:
            realtask = self.rqdata.runq_setscene[task]
            fn = self.rqdata.taskData.fn_index[self.rqdata.runq_fnid[realtask]]

            taskname = self.rqdata.runq_task[realtask] + "_setscene"
            if self.rq.check_stamp_task(realtask, self.rqdata.runq_task[realtask]):
                bb.msg.debug(2, bb.msg.domain.RunQueue, "Stamp for underlying task %s (%s) is current so skipping setscene varient" % (task, self.rqdata.get_user_idstring(task)))
                self.task_failoutright(task)
                return True

            if self.cooker.configuration.force:
                for target in self.rqdata.target_pairs:
                    if target[0] == fn and target[1] == self.rqdata.runq_task[realtask]:
                        self.task_failoutright(task)
                        return True

            if self.rq.check_stamp_task(realtask, taskname):
                bb.msg.debug(2, bb.msg.domain.RunQueue, "Setscene stamp current task %s (%s) so skip it and its dependencies" % (task, self.rqdata.get_user_idstring(realtask)))
                self.task_skip(task)
                return True

            bb.msg.note(1, bb.msg.domain.RunQueue,
                        "Running setscene task %d of %d (%s:%s)" % (self.stats.completed + self.stats.active + self.stats.failed + 1,
                                                                         self.stats.total, fn, taskname))

            proc, sockpid, sockfile = self.fork_off_task(fn, realtask, taskname)

            self.build_pids[proc.pid] = task
            self.build_procs[proc.pid] = proc
            self.build_pipes[proc.pid] = runQueuePipe(proc.stdout, proc.stdin, self.cfgData)
            self.build_sockpids[proc.pid] = sockpid
            self.build_sockfiles[proc.pid] = sockfile
            self.runq_running[task] = 1
            self.stats.taskActive()
            if self.stats.active < self.number_tasks:
                return True

        for pipe in self.build_pipes:
            self.build_pipes[pipe].read()

        if self.stats.active > 0:
            if self.runqueue_process_waitpid() is None:
                return 0.5
            return True

        # Convert scenequeue_covered task numbers into full taskgraph ids
        oldcovered = self.scenequeue_covered
        self.rq.scenequeue_covered = set()
        for task in oldcovered:
            self.rq.scenequeue_covered.add(self.rqdata.runq_setscene[task])

        bb.note("We can skip tasks %s" % self.rq.scenequeue_covered)

        self.rq.state = runQueueRunInit
        return True

class TaskFailure(Exception):
    """
    Exception raised when a task in a runqueue fails
    """
    def __init__(self, x):
        self.args = x


class runQueueExitWait(bb.event.Event):
    """
    Event when waiting for task processes to exit
    """

    def __init__(self, remain):
        self.remain = remain
        self.message = "Waiting for %s active tasks to finish" % remain
        bb.event.Event.__init__(self)

class runQueueEvent(bb.event.Event):
    """
    Base runQueue event class
    """
    def __init__(self, task, stats, rq):
        self.taskid = task
        self.taskstring = rq.rqdata.get_user_idstring(task)
        self.stats = stats
        bb.event.Event.__init__(self)

class runQueueTaskStarted(runQueueEvent):
    """
    Event notifing a task was started
    """
    def __init__(self, task, stats, rq):
        runQueueEvent.__init__(self, task, stats, rq)
        self.message = "Running task %s (%d of %d) (%s)" % (task, stats.completed + stats.active + 1, self.stats.total, self.taskstring)

class runQueueTaskFailed(runQueueEvent):
    """
    Event notifing a task failed
    """
    def __init__(self, task, stats, rq):
        runQueueEvent.__init__(self, task, stats, rq)
        self.message = "Task %s failed (%s)" % (task, self.taskstring)

class runQueueTaskCompleted(runQueueEvent):
    """
    Event notifing a task completed
    """
    def __init__(self, task, stats, rq):
        runQueueEvent.__init__(self, task, stats, rq)
        self.message = "Task %s completed (%s)" % (task, self.taskstring)

#def check_stamp_fn(fn, taskname, d):
#    rq = bb.data.getVar("__RUNQUEUE_DO_NOT_USE_EXTERNALLY", d)
#    fn = bb.data.getVar("__RUNQUEUE_DO_NOT_USE_EXTERNALLY2", d)
#    fnid = rq.rqdata.taskData.getfn_id(fn)
#    taskid = rq.get_task_id(fnid, taskname)
#    if taskid is not None:
#        return rq.check_stamp_task(taskid)
#    return None

class runQueuePipe():
    """
    Abstraction for a pipe between a worker thread and the server
    """
    def __init__(self, pipein, pipeout, d):
        self.fd = pipein
        pipeout.close()
        fcntl.fcntl(self.fd, fcntl.F_SETFL, fcntl.fcntl(self.fd, fcntl.F_GETFL) | os.O_NONBLOCK)
        self.queue = ""
        self.d = d

    def read(self):
        start = len(self.queue)
        try:
            self.queue = self.queue + self.fd.read(1024)
        except IOError:
            pass
        end = len(self.queue)
        index = self.queue.find("</event>")
        while index != -1:
            bb.event.fire_from_worker(self.queue[:index+8], self.d)
            self.queue = self.queue[index+8:]
            index = self.queue.find("</event>")
        return (end > start)

    def close(self):
        while self.read():
            continue
        if len(self.queue) > 0:
            print("Warning, worker left partial message: %s" % self.queue)
        self.fd.close()
