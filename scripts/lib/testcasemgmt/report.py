import os
import glob
import json
from testcasemgmt.gitstore import GitStore

class TextTestReport(object):

    def _get_test_result_files(self, git_dir, excludes, test_result_file):
        testresults = []
        for root, dirs, files in os.walk(git_dir, topdown=True):
            [dirs.remove(d) for d in list(dirs) if d in excludes]
            for name in files:
                if name == test_result_file:
                    testresults.append(os.path.join(root, name))
        return testresults

    def _load_json_test_results(self, file):
        if os.path.exists(file):
            with open(file, "r") as f:
                return json.load(f)
        else:
            return None

    def _map_raw_test_result_to_predefined_list(self, testresult):
        passed_list = ['PASSED', 'passed']
        failed_list = ['FAILED', 'failed', 'ERROR', 'error']
        skipped_list = ['SKIPPED', 'skipped']
        test_result = {'passed': 0, 'failed': 0, 'skipped': 0, 'failed_testcases': []}

        result = testresult["result"]
        for testcase in result.keys():
            test_status = result[testcase]["status"]
            if test_status in passed_list:
                test_result['passed'] += 1
            elif test_status in failed_list:
                test_result['failed'] += 1
                test_result['failed_testcases'].append(testcase)
            elif test_status in skipped_list:
                test_result['skipped'] += 1
        return test_result

    def _compute_test_result_percentage(self, test_result):
        total_tested = test_result['passed'] + test_result['failed'] + test_result['skipped']
        test_result['passed_percent'] = 0
        test_result['failed_percent'] = 0
        test_result['skipped_percent'] = 0
        if total_tested > 0:
            test_result['passed_percent'] = format(test_result['passed']/total_tested * 100, '.2f')
            test_result['failed_percent'] = format(test_result['failed']/total_tested * 100, '.2f')
            test_result['skipped_percent'] = format(test_result['skipped']/total_tested * 100, '.2f')

    def _convert_test_result_to_string(self, test_result):
        test_result['passed_percent'] = str(test_result['passed_percent'])
        test_result['failed_percent'] = str(test_result['failed_percent'])
        test_result['skipped_percent'] = str(test_result['skipped_percent'])
        test_result['passed'] = str(test_result['passed'])
        test_result['failed'] = str(test_result['failed'])
        test_result['skipped'] = str(test_result['skipped'])
        if 'idle' in test_result:
            test_result['idle'] = str(test_result['idle'])
        if 'idle_percent' in test_result:
            test_result['idle_percent'] = str(test_result['idle_percent'])
        if 'complete' in test_result:
            test_result['complete'] = str(test_result['complete'])
        if 'complete_percent' in test_result:
            test_result['complete_percent'] = str(test_result['complete_percent'])

    def _compile_test_result(self, testresult):
        test_result = self._map_raw_test_result_to_predefined_list(testresult)
        self._compute_test_result_percentage(test_result)
        self._convert_test_result_to_string(test_result)
        return test_result

    def _get_test_component(self, git_dir, file_dir):
        test_component = 'None'
        if git_dir != os.path.dirname(file_dir):
            test_component = file_dir.replace(git_dir + '/', '')
        return test_component

    def _get_max_string_len(self, test_result_list, key, default_max_len):
        max_len = default_max_len
        for test_result in test_result_list:
            value_len = len(test_result[key])
            if value_len > max_len:
                max_len = value_len
        return max_len

    def _render_text_test_report(self, template_file_name, test_result_list, max_len_component, max_len_config):
        from jinja2 import Environment, FileSystemLoader
        script_path = os.path.dirname(os.path.realpath(__file__))
        file_loader = FileSystemLoader(script_path + '/template')
        env = Environment(loader=file_loader, trim_blocks=True)
        template = env.get_template(template_file_name)
        output = template.render(test_reports=test_result_list,
                                 max_len_component=max_len_component,
                                 max_len_config=max_len_config)
        print('Printing text-based test report:')
        print(output)

    def view_test_report(self, logger, git_dir):
        test_result_list = []
        for test_result_file in self._get_test_result_files(git_dir, ['.git'], 'testresults.json'):
            logger.debug('Computing test result for test result file: %s' % test_result_file)
            testresults = self._load_json_test_results(test_result_file)
            for testresult_key in testresults.keys():
                test_result = self._compile_test_result(testresults[testresult_key])
                test_result['test_component'] = self._get_test_component(git_dir, test_result_file)
                test_result['test_configuration'] = testresult_key
                test_result['test_component_configuration'] = '%s_%s' % (test_result['test_component'],
                                                                         test_result['test_configuration'])
                test_result_list.append(test_result)
        max_len_component = self._get_max_string_len(test_result_list, 'test_component', len('test_component'))
        max_len_config = self._get_max_string_len(test_result_list, 'test_configuration', len('test_configuration'))
        self._render_text_test_report('test_report_full_text.txt', test_result_list, max_len_component, max_len_config)

def report(args, logger):
    gitstore = GitStore(args.git_dir, args.git_branch)
    if gitstore.check_if_git_dir_exist(logger):
        if gitstore.checkout_git_dir(logger):
            logger.debug('Checkout git branch: %s' % args.git_branch)
            testreport = TextTestReport()
            testreport.view_test_report(logger, args.git_dir)
    return 0

def register_commands(subparsers):
    """Register subcommands from this plugin"""
    parser_build = subparsers.add_parser('report', help='report test result summary',
                                         description='report text-based test result summary from the source git '
                                                     'directory with the given git branch',
                                         group='report')
    parser_build.set_defaults(func=report)
    parser_build.add_argument('git_branch', help='git branch to be used to compute test summary report')
    parser_build.add_argument('-d', '--git-dir', default='',
                              help='(optional) source directory to be used as git repository '
                                   'to compute test report where default location for source directory '
                                   'will be <top_dir>/testresults')
