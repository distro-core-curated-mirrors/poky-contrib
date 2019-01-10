# test case management tool - store test result
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
import json

class TestRegression(object):

    def _load_json_file(self, file):
        with open(file, "r") as f:
            return json.load(f)

    def _get_dict_value(self, dict, key):
        try:
            return True, dict[key]
        except KeyError:
            return False, 'KeyError exception: %s' % key
        except TypeError:
            return False, 'TypeError exception: dict=%s: key=%s' % (dict, key)

    def _get_test_result(self, logger, file, result_id):
        results = self._load_json_file(file)
        if not result_id:
            result_id = next(iter(results))
        status, result = self._get_dict_value(results, result_id)

        if not status:
            logger.error(result)
            return status
        logger.debug('Successfully get test result for file=%s: key=%s' % (file, result_id))
        return result

    def _show_test_status_diff(self, logger, base_result, target_result):
        print('============================Start Regression============================')
        print('If regression found different status between base and target, print below:')
        print('<test case> : <base status> -> <target status>')
        print('========================================================================')
        for k in base_result:
            status, base_testcase = self._get_dict_value(base_result, k)
            status, base_status = self._get_dict_value(base_testcase, 'status')
            if status:
                status, target_testcase = self._get_dict_value(target_result, k)
                if status:
                    status, target_status = self._get_dict_value(target_testcase, 'status')
                    if status:
                        if base_status != target_status:
                            print(k, ':', base_status, '->', target_status)
                    else:
                        logger.error('Faced exception during target test case status retrieval: %s' % target_status)
                        print(k, ':', base_status, '->', None)
                else:
                    logger.error('Faced exception during target test case retrieval: %s' % target_testcase)
                    print(k, ':', base_status, '->', None)
            else:
                logger.error('Faced exception during base test case status retrieval: %s' % base_status)

    def _perform_regression(self, logger, base_result, target_result):
        base_status, base_result = self._get_dict_value(base_result, 'result')
        target_status, target_result = self._get_dict_value(target_result, 'result')
        if base_status and target_status:
            logger.debug('Performing regression')
            self._show_test_status_diff(logger, base_result, target_result)
        else:
            if not base_status:
                logger.error(base_result)
            if not target_status:
                logger.error(target_result)

    def run(self, logger, base_result_file, target_result_file, base_result_id, target_result_id):
        base_result = self._get_test_result(logger, base_result_file, base_result_id)
        if base_result:
            target_result = self._get_test_result(logger, target_result_file, target_result_id)
            if target_result:
                self._perform_regression(logger, base_result, target_result)

def regression(args, logger):
    regression = TestRegression()
    regression.run(logger, args.base_result_file, args.target_result_file, args.base_result_id, args.target_result_id)
    return 0

def register_commands(subparsers):
    """Register subcommands from this plugin"""
    parser_build = subparsers.add_parser('regression', help='regression analysis',
                                         description='regression analysis comparing base result set to target '
                                                     'result set',
                                         group='analysis')
    parser_build.set_defaults(func=regression)
    parser_build.add_argument('base_result_file',
                              help='base result file provide the base result set')
    parser_build.add_argument('target_result_file',
                              help='target result file provide the target result set for comparison with base set')
    parser_build.add_argument('-b', '--base-result-id', default='',
                              help='(optional) default select the first result set available unless base result id '
                                   'was provided')
    parser_build.add_argument('-t', '--target-result-id', default='',
                              help='(optional) default select the first result set available unless target result id '
                                   'was provided')
