import os
import unittest
from testresultlog.testresultgitstore import TestResultGitStore
from testresultlog.testlogparser import TestLogParser

class TestResultUpdator(object):

    # def __init__(self):
    #     self.script_path = os.path.dirname(os.path.realpath(__file__))
    #     self.base_path = self.script_path + '/../../..'

    def _get_testsuite_from_testcase(self, testcase):
        testsuite = testcase[0:testcase.rfind(".")]
        return testsuite

    def _get_testmodule_from_testsuite(self, testsuite):
        testmodule = testsuite[0:testsuite.find(".")]
        return testmodule

    def _remove_testsuite_from_testcase(self, testcase, testsuite):
        testsuite = testsuite + '.'
        testcase_remove_testsuite = testcase.replace(testsuite, '')
        return testcase_remove_testsuite

    # def _get_oeqa_source_dir(self, source):
    #     if source == 'runtime':
    #         oeqa_dir = os.path.join(self.base_path, 'meta/lib/oeqa/runtime/cases')
    #     elif source == 'selftest':
    #         oeqa_dir = os.path.join(self.base_path, 'meta/lib/oeqa/selftest/cases')
    #     elif source == 'sdk':
    #         oeqa_dir = os.path.join(self.base_path, 'meta/lib/oeqa/sdk/cases')
    #     else:
    #         oeqa_dir = os.path.join(self.base_path, 'meta/lib/oeqa/sdkext/cases')
    #     return oeqa_dir

    def _discover_unittest_testsuite_testcase(self, test_dir):
        loader = unittest.TestLoader()
        testsuite_testcase = loader.discover(start_dir=test_dir, pattern='*.py')
        return testsuite_testcase

    def _generate_flat_list_of_unittest_testcase(self, testsuite):
        for test in testsuite:
            if unittest.suite._isnotsuite(test):
                yield test
            else:
                for subtest in self._generate_flat_list_of_unittest_testcase(test):
                    yield subtest

    def _get_testsuite_from_unittest_testcase(self, unittest_testcase):
        testsuite = unittest_testcase[unittest_testcase.find("(")+1:unittest_testcase.find(")")]
        return testsuite

    def _get_testcase_from_unittest_testcase(self, unittest_testcase):
        testcase = unittest_testcase[0:unittest_testcase.find("(")-1]
        testsuite = self._get_testsuite_from_unittest_testcase(unittest_testcase)
        testcase = '%s.%s' % (testsuite, testcase)
        return testcase

    def _get_testmodule_from_testsuite(self, testsuite):
        testmodule = testsuite[0:testsuite.find(".")]
        return testmodule

    def _add_new_environment_to_environment_list(self, environment_list, new_environment):
        if len(new_environment) > 0 and new_environment not in environment_list:
            if len(environment_list) == 0:
                environment_list = new_environment
            else:
                environment_list = '%s,%s' % (environment_list, new_environment)
        return environment_list

    def get_environment_list_for_test_log(self, log_file, log_file_source, environment_list, testlogparser):
        print('Getting test environment information from test log at %s' % log_file)
        if log_file_source == 'runtime':
            runtime_image_env = testlogparser.get_runtime_test_image_environment(log_file)
            print('runtime image environment: %s' % runtime_image_env)
            runtime_qemu_env = testlogparser.get_runtime_test_qemu_environment(log_file)
            print('runtime qemu environment: %s' % runtime_qemu_env)
            environment_list = self._add_new_environment_to_environment_list(environment_list, runtime_image_env)
            environment_list = self._add_new_environment_to_environment_list(environment_list, runtime_qemu_env)
        return environment_list.split(",")

    def get_testsuite_testcase_dictionary(self, work_dir):
        print('Getting testsuite testcase information from oeqa directory at %s' % work_dir)
        unittest_testsuite_testcase = self._discover_unittest_testsuite_testcase(work_dir)
        unittest_testcase_list = self._generate_flat_list_of_unittest_testcase(unittest_testsuite_testcase)
        testsuite_testcase_dict = {}
        for unittest_testcase in unittest_testcase_list:
            testsuite = self._get_testsuite_from_unittest_testcase(str(unittest_testcase))
            testcase = self._get_testcase_from_unittest_testcase(str(unittest_testcase))
            if testsuite in testsuite_testcase_dict:
                testsuite_testcase_dict[testsuite].append(testcase)
            else:
                testsuite_testcase_dict[testsuite] = [testcase]
        return testsuite_testcase_dict

    def get_testmodule_testsuite_dictionary(self, testsuite_testcase_dict):
        print('Getting testmodule testsuite information')
        testsuite_list = testsuite_testcase_dict.keys()
        testmodule_testsuite_dict = {}
        for testsuite in testsuite_list:
            testmodule = self._get_testmodule_from_testsuite(testsuite)
            if testmodule in testmodule_testsuite_dict:
                testmodule_testsuite_dict[testmodule].append(testsuite)
            else:
                testmodule_testsuite_dict[testmodule] = [testsuite]
        return testmodule_testsuite_dict

    def get_testcase_failed_or_error_logs_dictionary(self, log_file, testcase_status_dict):
        print('Getting testcase failed or error log from %s' % log_file)
        testlogparser = TestLogParser()
        testcase_list = testcase_status_dict.keys()
        testcase_failed_or_error_logs_dict = {}
        for testcase in testcase_list:
            test_status = testcase_status_dict[testcase]
            if test_status == 'FAILED' or test_status == 'ERROR':
                testsuite = self._get_testsuite_from_testcase(testcase)
                testfunction = self._remove_testsuite_from_testcase(testcase, testsuite)
                logs = testlogparser.get_test_log(log_file, test_status, testfunction, testsuite)
                testcase_failed_or_error_logs_dict[testcase] = logs
        return testcase_failed_or_error_logs_dict

def main(args):
    testlogparser = TestLogParser()
    testcase_status_dict = testlogparser.get_test_status(args.log_file)

    testresultupdator = TestResultUpdator()
    environment_list = testresultupdator.get_environment_list_for_test_log(args.log_file, args.source, args.environment_list, testlogparser)
    testsuite_testcase_dict = testresultupdator.get_testsuite_testcase_dictionary(args.oeqa_dir)
    testmodule_testsuite_dict = testresultupdator.get_testmodule_testsuite_dictionary(testsuite_testcase_dict)
    test_logs_dict = testresultupdator.get_testcase_failed_or_error_logs_dictionary(args.log_file, testcase_status_dict)

    testresultstore = TestResultGitStore()
    testresultstore.smart_update_automated_test_result(args.git_repo, args.git_branch, args.component, environment_list, testmodule_testsuite_dict, testsuite_testcase_dict, testcase_status_dict, test_logs_dict)
    if (len(args.git_remote) > 0):
        testresultstore.git_remote_fetch_rebase_push(args.git_repo, args.git_branch, args.git_remote)

def register_commands(subparsers):
    """Register subcommands from this plugin"""
    parser_build = subparsers.add_parser('update', help='Update test result status into the specified test result template',
                                         description='Update test result status from the test log into the specified test result template')
    parser_build.set_defaults(func=main)
    parser_build.add_argument('-l', '--log_file', required=True, help='Full path to the test log file to be used for test result update')
    parser_build.add_argument('-g', '--git_repo', required=False, default='default', help='(Optional) Git repository to be updated ,default will be <top_dir>/test-result-log-git')
    parser_build.add_argument('-b', '--git_branch', required=True, help='Git branch to be updated with test result')
    parser_build.add_argument('-r', '--git_remote', required=False, default='', help='(Optional) Git remote repository to be updated')
    SOURCE = ('runtime', 'selftest', 'sdk', 'sdkext')
    parser_build.add_argument('-s', '--source', required=True, choices=SOURCE,
    help='Testcase source to be selected from the list (runtime, selftest, sdk or sdkext). '
         '"runtime" will search testcase available in meta/lib/oeqa/runtime/cases. '
         '"selftest" will search testcase available in meta/lib/oeqa/selftest/cases. '
         '"sdk" will search testcase available in meta/lib/oeqa/sdk/cases. '
         '"sdkext" will search testcase available in meta/lib/oeqa/sdkext/cases. ')
    parser_build.add_argument('-d', '--poky_dir', required=False, default='default', help='(Optional) Poky directory to be used for oeqa testcase(s) discovery, default will use current poky directory')
    parser_build.add_argument('-c', '--component', required=True, help='Component selected (as the top folder) to store the related test environments')
    parser_build.add_argument('-e', '--environment_list', required=False, default='', help='List of environment to be used to perform update')