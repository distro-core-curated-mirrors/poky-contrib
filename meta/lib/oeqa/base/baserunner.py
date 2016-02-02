#!/usr/bin/env python
# Copyright (C) 2013 Intel Corporation
#
# Released under the MIT license (see COPYING.MIT)

# Base unittest module used by testrunner
# This provides the common test runner functionalities including manifest input,
# xunit output, timeout, tag filtering.

"""Base testrunner"""

import os
import sys
import time
import unittest
import shutil
from optparse import OptionParser, make_option
from util.log import LogHandler
from util.tag import filter_tagexp
from util.timeout import set_timeout


class TestContext(object):
    '''test context which inject into testcase'''
    def __init__(self):
        self.target = None
        

class TestRunnerBase(object):
    '''test runner base '''
    def __init__(self, context=None, runner=None):
        self.runner = runner if runner else unittest.TextTestRunner(stream=sys.stderr, verbosity=2)
        self.context = context if context else TestContext()
        self.tclist = getattr(self.context, "testslist", [])
        self.test_result = None
        setattr(unittest.TestCase, "tc", self.context)

    def configure(self, options=None):
        '''configure before testing'''
        pass

    def loadtest(self, names=None):
        '''load test suite'''
        if not names:
            names = self.tclist
        testloader = unittest.TestLoader()
        tclist = []
        for name in names:
            tset = testloader.loadTestsFromName(name)
            if tset.countTestCases() > 0:
                tclist.append(tset)
            elif tset._tests == []:
                tclist.append(testloader.discover(name, "[!_]*.py"))
        return testloader.suiteClass(tclist)

    def filtertest(self, testsuite):
        '''filter test set'''
        if self.context.tagexp:
            return filter_tagexp(testsuite, self.context.tagexp)
        return testsuite

    def runtest(self, testsuite):
        '''run test suite'''
        self.test_result = self.runner.run(testsuite)

    def start(self, testsuite):
        '''start testing'''
        setattr(unittest.TestCase, "tc", self.context)
        self.runtest(testsuite)

class TestProgram(object):
    runner_class = TestRunnerBase

    def __init__(self):
        self.option_list = []
        self.context = TestContext()
        self.run()

    def options(self):
        self.option_list = [
            make_option("-f", "--manifest", dest="manifest",
                    help="The test list file"),
            make_option("-x", "--xunit", dest="xunit",
                    help="Output result path of in xUnit XML format"),
            make_option("-l", "--log-dir", dest="logdir",
                    help="Set log dir."),
            make_option("-a", "--tag-expression", dest="tag",
                    help="Set tag expression to filter test cases."),
            make_option("-T", "--timeout", dest="timeout",
                    help="Set timeout for each test case."),
            make_option("-e", "--tests", dest="tests", action="append",
                    help="Run tests by dot separated module path")
        ]

    @staticmethod
    def __get_tc_from_manifest(fname):
        '''get tc list from manifest format '''
        with open(fname, "r") as f:
            tclist = [n.strip() for n in f.readlines() \
                                if n.strip() and not n.strip().startswith('#')]
        return tclist

    @staticmethod
    def _get_log_dir(logdir):
        '''get the log directory'''
        if os.path.exists(logdir):
            shutil.rmtree(logdir)
        os.makedirs(logdir)
        return logdir

    def get_options(self, default=False):
        '''handle testrunner options'''
        self.parser = OptionParser(option_list=self.option_list, \
                                usage="usage: %prog [options]")
        if default:
            return self.parser.parse_args(args=[])
        return self.parser.parse_args()

    def configure(self, options=None):
        '''configure before testing'''
        self.test_options = options
        options, args = options if isinstance(options, tuple) else (options, None)
        if options.xunit:
            try:
                from xmlrunner import XMLTestRunner
            except ImportError:
                raise Exception("unittest-xml-reporting not installed")
            self.context.runner = XMLTestRunner(stream=sys.stderr, \
                                        verbosity=2, output=options.xunit)
        else:
            self.context.runner = unittest.TextTestRunner(stream=sys.stderr, \
                                                  verbosity=2)

        if options.manifest:
            print options.manifest
            fbname, fext = os.path.splitext(os.path.basename(options.manifest))
            assert fbname == "manifest" or fext == ".manifest", \
                  "Please specify file name like xxx.manifest or manifest.xxx"
            self.context.testslist = self.__get_tc_from_manifest(options.manifest)

        if options.tests:
            self.context.testslist.extend(options.tests)

        self.context.tagexp = options.tag

        if options.logdir:
            logdir = self._get_log_dir(options.logdir)
            self.log_handler = LogHandler(logdir)

        try:
            self.context.def_timeout = int(options.timeout) if options.timeout else None
        except ValueError:
            print "timeout need an integer value"
            raise

    def make_runner(self):
        self.runner = self.runner_class(self.context)
        return self.runner

    def run(self):
        self.options()
        options = self.get_options()
        self.configure(options)
        runner = self.make_runner()
        runner.configure(options)
        suite = runner.filtertest(runner.loadtest())
        print "Found %s tests" % suite.countTestCases()
        set_timeout(suite, self.context.def_timeout)
        runner.start(suite)

main = TestProgram
if __name__ == "__main__":
    main()
