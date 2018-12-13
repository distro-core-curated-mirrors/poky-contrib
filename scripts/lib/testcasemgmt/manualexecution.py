# test case management tool - manual execution from testopia test cases
#
# Copyright (c) 2018, Intel Corporation.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
import argparse
import json
import os
import sys
import datetime
import re
from oeqa.core.runner import OETestResultJSONHelper

class ManualTestRunner(object):
    def __init__(self):
        self.jdata = ''
        self.test_module = ''
        self.test_suite = ''
        self.test_case = ''
        self.configuration = ''
        self.starttime = ''
        self.result_id = ''
        self.write_dir = ''

    def _read_json(self, file):
        self.jdata = json.load(open('%s' % file))
        self.test_case = []
        self.test_module = self.jdata[0]['test']['@alias'].split('.', 2)[0]
        self.test_suite = self.jdata[0]['test']['@alias'].split('.', 2)[1]
        for i in range(0, len(self.jdata)):
            self.test_case.append(self.jdata[i]['test']['@alias'].split('.', 2)[2])
        return self.jdata, self.test_module, self.test_suite, self.test_case
    
    def _get_input(self, config):
        while True:
            output = input('{} = '.format(config))
            if re.match('^[a-zA-Z0-9_]+$', output):
                break
            print('Only alphanumeric and underscore are allowed. Please try again')
        return output

    def _create_config(self):
        self.configuration = {}
        while True:
            try:
                conf_total = int(input('\nPlease provide how many configuration you want to save \n'))
                break
            except ValueError:
                print('Invalid input. Please provide input as a number not character.')
        for i in range(conf_total):
            print('---------------------------------------------')
            print('This is your %s ' % (i + 1) + 'configuration. Please provide configuration name and its value')
            print('---------------------------------------------')
            name_conf = self._get_input('Configuration Name')
            value_conf = self._get_input('Configuration Value')
            print('---------------------------------------------\n')
            self.configuration[name_conf.upper()] = value_conf
        current_datetime = datetime.datetime.now()
        self.starttime = current_datetime.strftime('%Y%m%d%H%M%S')
        self.configuration['STARTTIME'] = self.starttime
        self.configuration['TEST_TYPE'] = self.test_module
        return self.configuration

    def _create_result_id(self):
        self.result_id = 'manual_' + self.test_module + '_' + self.starttime
        return self.result_id

    def _execute_test_steps(self, test_id):
        test_result = {}
        testcase_id = self.test_module + '.' + self.test_suite + '.' + self.test_case[test_id]
        print('------------------------------------------------------------------------')
        print('Executing test case:' + '' '' + self.test_case[test_id])
        print('------------------------------------------------------------------------')
        print('You have total ' + max(self.jdata[test_id]['test']['execution'].keys()) + ' test steps to be executed.')
        print('------------------------------------------------------------------------\n')

        for step in range(1, int(max(self.jdata[test_id]['test']['execution'].keys()) + '1')):
            print('Step %s: ' % step + self.jdata[test_id]['test']['execution']['%s' % step]['action'])
            print('Expected output: ' + self.jdata[test_id]['test']['execution']['%s' % step]['expected_results'])
            if step == int(max(self.jdata[test_id]['test']['execution'].keys())):
                done = input('\nPlease provide test results: (P)assed/(F)ailed/(B)locked? \n')
                break
            else:
                done = input('\nPlease press ENTER when you are done to proceed to next step.\n')

        if done == 'p' or done == 'P':
            res = 'PASSED'
        elif done == 'f' or done == 'F':
            res = 'FAILED'
            log_input = input('\nPlease enter the error and the description of the log: (Ex:log:211 Error Bitbake)\n')
        elif done == 'b' or done == 'B':
            res = 'BLOCKED'
        else:
            res = 'SKIPPED'
            
        if res == 'FAILED':
            test_result.update({testcase_id: {'status': '%s' % res, 'log': '%s' % log_input}})
        else:
            test_result.update({testcase_id: {'status': '%s' % res}})
        return test_result

    def _create_write_dir(self):
        basepath = os.environ['BUILDDIR']
        self.write_dir = basepath + '/tmp/log/manual/'
        sys.path.insert(0, self.write_dir)

    def run_test(self, file):
        self._read_json(file)
        self._create_config()
        self._create_result_id()
        self._create_write_dir()
        test_results = {}
        print('\nTotal number of test cases in this test suite: ' + '%s\n' % len(self.jdata))
        for i in range(0, len(self.jdata)):
            test_result = self._execute_test_steps(i)
            test_results.update(test_result)
        return self.configuration, self.result_id, self.write_dir, test_results

def manualexecution(args, logger):
    testrunner = ManualTestRunner()
    get_configuration, get_result_id, get_write_dir, get_test_results = testrunner.run_test(args.file)
    resultjsonhelper = OETestResultJSONHelper()
    resultjsonhelper.dump_testresult_file(get_write_dir, get_configuration, get_result_id,
                                          get_test_results)
    return 0

def register_commands(subparsers):
    """Register subcommands from this plugin"""
    parser_build = subparsers.add_parser('manualexecution', help='Helper script for results populating during manual test execution.',
                                         description='Helper script for results populating during manual test execution. You can find manual test case JSON file in meta/lib/oeqa/manual/',
                                         group='manualexecution')
    parser_build.set_defaults(func=manualexecution)
    parser_build.add_argument('file', help='Specify path to manual test case JSON file.Note: Please use \"\" to encapsulate the file path.')