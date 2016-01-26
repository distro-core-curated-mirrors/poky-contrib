#!/usr/bin/env python
# Copyright (C) 2013 Intel Corporation
#
# Released under the MIT license (see COPYING.MIT)

# test runner which support run testing on target device

"""test runner for target device"""
import sys
from optparse import make_option
from baserunner import TestRunnerBase

class TargetTestRunner(TestRunnerBase):
    '''test runner which support target DUT access'''
    def __init__(self, context=None):
        super(TargetTestRunner, self).__init__(context)

    def runtest(self, testsuite):
        ret = None
        if getattr(self.context, "target", None):
            getattr(self.context, "target").deploy()
            getattr(self.context, "target").start()
        try:
            ret = super(TargetTestRunner, self).runtest(testsuite)
        finally:
            if getattr(self.context, "target", None):
                getattr(self.context, "target").stop()
        return ret
