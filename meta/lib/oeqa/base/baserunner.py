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
import unittest
from optparse import OptionParser, make_option

class TestContext(object):
    '''test context which inject into testcase'''
    def __init__(self):
        self.target = None

class TestRunnerBase(object):
    '''test runner base '''
    def __init__(self):
        self.option_list = []
        self.tclist = []
        self.runner = None
        self.context = None
        self.manifest = None

    @staticmethod
    def __get_tc_from_manifest(fname):
        '''get tc list from manifest format '''
        with open(fname, "r") as f:
            tclist = [{"id":n.strip()} for n in f.readlines() \
                                if n.strip() and not n.strip().startswith('#')]
        return tclist

    def options(self):
        '''handle testrunner options'''
        self.option_list = [
            make_option("-f", "--manifest", dest="manifest",
                    help="The test list file"),
            make_option("-x", "--xunit", dest="xunit",
                    help="Output result path of in xUnit XML format"),
        ]

    def configure(self, options):
        '''configure before testing'''
        if options.xunit:
            try:
                from xmlrunner import XMLTestRunner
            except ImportError:
                raise Exception("unittest-xml-reporting not installed")
            self.runner = XMLTestRunner(stream=sys.stderr, \
                                        verbosity=2, output=options.xunit)
        else:
            self.runner = unittest.TextTestRunner(stream=sys.stderr, \
                                                  verbosity=2)

        self.tclist = []
        if options.manifest:
            self.manifest = options.manifest
            fext = os.path.splitext(options.manifest)[1]
            assert fext == ".manifest", "Please use specify a manifest file \
                                      with .manifest postfix"
            self.tclist = self.__get_tc_from_manifest(options.manifest)
        else:
            raise Exception("please specify a manifest file by -f")

        self.context = TestContext()

    def result(self):
        '''output test result '''
        print "output test result..."
        print self.tclist

    def start(self):
        '''start execution'''
        setattr(unittest.TestCase, "tc", self.context)
        testloader = unittest.TestLoader()
        testloader.sortTestMethodsUsing = None
        tnames = [tc["id"] for tc in self.tclist]
        suite = testloader.loadTestsFromNames(tnames)
        print "Found %s tests" % suite.countTestCases()
        self.runner.run(suite)

    def run(self):
        '''run test suite'''
        self.options()
        usage = "usage: %prog [options]"
        parser = OptionParser(option_list=self.option_list, usage=usage)
        options = parser.parse_args()[0]
        self.configure(options)
        print options
        self.start()
        self.result()

if __name__ == "__main__":
    TestRunnerBase().run()
