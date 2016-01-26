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


class TestContext(object):
    '''test context which inject into testcase'''
    def __init__(self):
        self.target = None
        

class TestRunnerBase(object):
    '''test runner base '''
    def __init__(self, context=None):
        self.tclist = []
        self.runner = None
        self.context = context if context else TestContext()
        self.test_result = None

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

    def runtest(self, testsuite):
        '''run test suite'''
        self.test_result = self.runner.run(testsuite)

    def start(self, testsuite):
        '''start testing'''
        setattr(unittest.TestCase, "tc", self.context)
        self.runtest(testsuite)
