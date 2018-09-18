#!/usr/bin/python
#
# DESCRIPTION
# This is main script for running all selected toaster cases
# on selected web browser manifested in toaster_test.cfg
#

import argparse
import ConfigParser
import os
import platform
import sys
from toaster_automation_test import toaster_cases
import unittest

def get_args_parser():
    description = "Script that runs toaster auto tests."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--run-all-tests', required=False, action="store_true", dest="run_all_tests", default=False,
                       help='Run all tests.')
    parser.add_argument('--run-suite', required=False, dest='run_suite', default=False,
                       help='run suite (defined in cfg file)')
    return parser

def get_tests():
    testslist = []
    prefix = 'toaster_automation_test.toaster_cases'
    for t in dir(toaster_cases):
        if t.startswith('test_'):
            testslist.append('.'.join((prefix, t)))
    return testslist

def get_tests_from_cfg(suite=None):

    testslist = []
    config = ConfigParser.SafeConfigParser()
    config.read('toaster_test.cfg')

    if suite is not None:
        target_suite = suite.lower()
    else:
        target_suite = platform.system().lower()
    try:
        tests_from_cfg = eval(config.get('toaster_test_' + target_suite, 'test_cases'))
    except:
        print('Failed to get test cases from cfg file. Make sure the format is correct.')
        return None

    prefix = 'toaster_automation_test.toaster_cases.test_'
    for t in tests_from_cfg:
        testslist.append(prefix + str(t))
    return testslist

def buildResultClass(args):
    """Build a Result Class to use in the testcase execution"""
    class StampedResult(unittest.TextTestResult):
        """
        Custom TestResult that prints the time when a test starts.  As toaster-auto
        can take a long time (ie a few hours) to run, timestamps help us understand
        what tests are taking a long time to execute.
        """
        def startTest(self, test):
            import time
            self.stream.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " - ")
            super(StampedResult, self).startTest(test)
    return StampedResult

def main():

    os.chdir(os.path.abspath(sys.path[0]))
    parser = get_args_parser()
    args = parser.parse_args()

    if args.run_all_tests:
        testslist = get_tests()
    elif args.run_suite:
        testslist = get_tests_from_cfg(args.run_suite)
        os.environ['TOASTER_SUITE'] = args.run_suite
    else:
        testslist = get_tests_from_cfg()

    if not testslist:
        print('Failed to get test cases.')
        exit(1)

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = None
    runner = unittest.TextTestRunner(verbosity=2, resultclass=buildResultClass(args))
    for test in testslist:
        try:
            suite.addTests(loader.loadTestsFromName(test))
        except:
            return 1

    result = runner.run(suite)

    if result.wasSuccessful():
        return 0
    else:
        return 1

if __name__ == "__main__":

    try:
        ret = main()
    except:
        ret = 1
        import traceback
        traceback.print_exc()
    finally:
        if os.getenv('TOASTER_SUITE'):
            del os.environ['TOASTER_SUITE']
    sys.exit(ret)