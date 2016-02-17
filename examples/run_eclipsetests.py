#!/usr/bin/python

# Copyright

# DESCRIPTION
# This is script for running all selected eclipse cases on
# selected web browsers manifested in toaster_test.cfg.


import unittest, time, sys, os, logging, platform
import ConfigParser
import subprocess
import argparse
from eclipse_automation_test import eclipse_cases

def get_args_parser():
    description = "Script that runs eclipse auto tests."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--run-all-tests', required=False, action="store_true", dest="run_all_tests", default=False, help='Run all (unhidden) tests')
    parser.add_argument('--list-tests', required=False,  action="store_true", dest="list_tests", default=False,
                       help='List all available tests.')
    parser.add_argument('--run-suite', required=False, dest='run_suite', default=False,
                       help='run suite (defined in ini file)')
    return parser


def get_tests():

    testslist = []
    prefix = 'eclipse_automation_test.eclipse_cases'

    for t in dir(eclipse_cases):
        if t.startswith('test_'):
            testslist.append('.'.join((prefix, t)))

    return testslist


def get_tests_from_ini(suite=None):

    testslist = []
    config = ConfigParser.SafeConfigParser()
    config.read('settings-eclipse.ini')

    if suite is not None:
        target_suite = suite.lower()

        # TODO: if suite is valid suite

    else:
        target_suite = platform.system().lower()

    try:
        tests_from_ini = eval(config.get('eclipse_test_' + target_suite, 'test_cases'))
    except:
        print 'Failed to get test cases from ini file. Make sure the format is correct.'
        return None

    prefix = 'eclipse_automation_test.eclipse_cases.test_'
    for t in tests_from_ini:
        testslist.append(prefix + str(t))

    return testslist

def main():

# In case this script is called from other directory
    os.chdir(os.path.abspath(sys.path[0]))

    parser = get_args_parser()
    args = parser.parse_args()


    if args.run_all_tests:
        testslist = get_tests()
    elif args.run_suite:
        testslist = get_tests_from_ini(args.run_suite)
        os.environ['ECLIPSE_SUITE'] = args.run_suite
    else:
        testslist = get_tests_from_ini()

    if not testslist:
        print 'Failed to get test cases.'
        exit(1)

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = None
    runner = unittest.TextTestRunner(verbosity=2, resultclass=buildResultClass(args))

    for test in testslist:
        try:
            suite.addTests(loader.loadTestsFromName(test))
        except AttributeError as e:
            return 1

    result = runner.run(suite)

    if result.wasSuccessful():
        return 0
    else:
        return 1


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


if __name__ == "__main__":


    try:
        ret = main()
    except:
        ret = 1
        import traceback
        traceback.print_exc(5)
    finally:
        if os.getenv('ECLIPSE_SUITE'):
            del os.environ['ECLIPSE_SUITE']
    sys.exit(ret)


