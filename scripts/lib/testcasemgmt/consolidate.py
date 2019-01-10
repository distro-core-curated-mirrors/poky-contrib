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
import os
import json

class TestConsolidate(object):

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

    def _get_test_results(self, logger, file, result_id):
        results = self._load_json_file(file)
        if result_id:
            status, result = self._get_dict_value(results, result_id)
            if not status:
                logger.error('Faced exception during get test results: %s' % result)
                return status
            return {result_id: result}
        return results

    def _get_write_dir(self):
        basepath = os.environ['BUILDDIR']
        return basepath + '/tmp/'

    def _write_file(self, write_dir, file_name, file_content):
        file_path = os.path.join(write_dir, file_name)
        with open(file_path, 'w') as the_file:
            the_file.write(file_content)

    def _perform_consolidation(self, base_results, target_results, output_dir):
        for k in target_results:
            base_results[k] = target_results[k]
        json_testresults = json.dumps(base_results, sort_keys=True, indent=4)
        file_output_dir = output_dir if output_dir else self._get_write_dir()
        self._write_file(file_output_dir, 'testresults.json', json_testresults)
        print('Successfully consolidated results to: %s' % os.path.join(file_output_dir, 'testresults.json'))

    def run(self, logger, base_result_file, target_result_file, target_result_id, output_dir):
        base_results = self._get_test_results(logger, base_result_file, '')
        if base_results:
            target_results = self._get_test_results(logger, target_result_file, target_result_id)
            if target_results:
                self._perform_consolidation(base_results, target_results, output_dir)

def consolidate(args, logger):
    consolidate = TestConsolidate()
    consolidate.run(logger, args.base_result_file, args.target_result_file, args.target_result_id, args.output_dir)
    return 0

def register_commands(subparsers):
    """Register subcommands from this plugin"""
    parser_build = subparsers.add_parser('consolidate', help='consolidate results',
                                         description='consolidate results from multiple files',
                                         group='consolidate')
    parser_build.set_defaults(func=consolidate)
    parser_build.add_argument('base_result_file',
                              help='base result file provide the base result set')
    parser_build.add_argument('target_result_file',
                              help='target result file provide the target result set for consolidation into the '
                                   'base set')
    parser_build.add_argument('-t', '--target-result-id', default='',
                              help='(optional) default consolidate all result sets available unless specific target  '
                                   'result id was provided')
    parser_build.add_argument('-o', '--output-dir', default='',
                              help='(optional) default consolidate results to <poky>/build/tmp/ unless specific  '
                                   'output directory was provided')

