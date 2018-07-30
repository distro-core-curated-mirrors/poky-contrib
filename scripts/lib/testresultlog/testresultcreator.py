import os
from testresultlog.testresultlogconfigparser import TestResultLogConfigParser
from testresultlog.oeqatestcasecreator import OeqaTestCaseCreator
from testresultlog.testresultgitstore import TestResultGitStore

class TestPlanCreator(object):

    def _get_test_configuration_list(self, conf_path, section):
        config_parser = TestResultLogConfigParser(conf_path)
        return config_parser.get_config_items(section)

    def _init_environment_multiplication_matrix(self, env_matrix, new_env_list):
        for env in new_env_list:
            env_matrix.append(env)

    def _multiply_current_env_list_with_new_env_list(self, cur_env_list, new_env_list):
        multiplied_list = []
        for cur_env in cur_env_list:
            for new_env in new_env_list:
                multiplied_list.append('%s,%s' % (cur_env, new_env))
        return multiplied_list

    def _get_testsuite_from_testcase(self, testcase):
        testsuite = testcase[0:testcase.rfind(".")]
        return testsuite

    def _get_testmodule_from_testsuite(self, testsuite):
        testmodule = testsuite[0:testsuite.find(".")]
        return testmodule

    def get_test_environment_multiplication_matrix(self, test_component, component_conf, environment_conf):
        print('Getting test environment key(s) at %s for component (%s)' % (component_conf, test_component))
        test_environment_list = self._get_test_configuration_list(component_conf, test_component)
        print('test environment key(s): %s' % test_environment_list)
        env_matrix = []
        for env in test_environment_list:
            print('Getting test environment value(s) at %s for key (%s)' % (environment_conf, env))
            env_value_list = self._get_test_configuration_list(environment_conf, env)
            print('test environment value(s): %s' % env_value_list)
            if len(env_matrix) == 0:
                self._init_environment_multiplication_matrix(env_matrix, env_value_list, env)
            else:
                env_matrix = self._multiply_current_env_list_with_new_env_list(env_matrix, env_value_list, env)
        return env_matrix

    def get_testsuite_testcase_dictionary(self, work_dir, testcase_remove_source_file):
        print('Getting testsuite testcase information from oeqa directory at %s' % work_dir)
        oeqatestcasecreator = OeqaTestCaseCreator()
        testcase_list = oeqatestcasecreator.get_oeqa_testcase_list(work_dir, testcase_remove_source_file)
        testsuite_testcase_dict = {}
        for testcase in testcase_list:
            testsuite = self._get_testsuite_from_testcase(testcase)
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

def main(args):
    scripts_path = os.path.dirname(os.path.realpath(__file__))
    component_conf = os.path.join(scripts_path, 'conf/testplan_component.conf')
    environment_conf = os.path.join(scripts_path, 'conf/testplan_component_environment.conf')

    testplan_creator = TestPlanCreator()
    test_env_matrix = testplan_creator.get_test_environment_multiplication_matrix(args.component, component_conf, environment_conf)
    testsuite_testcase_dict = testplan_creator.get_testsuite_testcase_dictionary(args.oeqa_dir, args.testcase_remove_source_file)
    testmodule_testsuite_dict = testplan_creator.get_testmodule_testsuite_dictionary(testsuite_testcase_dict)

    for env in test_env_matrix:
        env_list = env.split(",")
        testresultstore = TestResultGitStore()
        testresultstore.create_automated_test_result(args.git_repo, args.git_branch, args.component, env_list, testmodule_testsuite_dict, testsuite_testcase_dict, args.force_create)

def register_commands(subparsers):
    """Register subcommands from this plugin"""
    parser_build = subparsers.add_parser('create', help='Create testplan and test result template',
                                         description='Create testplan and test result template based on environment configuration inside testresultlog/conf/testplan_component.conf and testresultlog/conf/testplan_component_environment.conf')
    parser_build.set_defaults(func=main)
    SOURCE = ('runtime', 'selftest', 'sdk', 'sdkext')
    parser_build.add_argument('-s', '--source', required=True, choices=SOURCE,
    help='Testcase source to be selected from the list (runtime, selftest, sdk or sdkext). '
         '"runtime" will search testcase available in meta/lib/oeqa/runtime/cases. '
         '"selftest" will search testcase available in meta/lib/oeqa/selftest/cases. '
         '"sdk" will search testcase available in meta/lib/oeqa/sdk/cases. '
         '"sdkext" will search testcase available in meta/lib/oeqa/sdkext/cases. ')
    parser_build.add_argument('-d', '--poky_dir', required=False, default='default', help='(Optional) Poky directory to be used for oeqa testcase(s) discovery, default will use current poky directory')
    parser_build.add_argument('-c', '--component', required=True, help='Component to be selected from testresultlog/conf/testplan_component.conf for creation of test environments')
    parser_build.add_argument('-g', '--git_repo', required=False, default='default', help='(Optional) Git repository to be created, default will be <top_dir>/test-result-log-git')
    parser_build.add_argument('-b', '--git_branch', required=True, help='Git branch to be created for the git repository')
    parser_build.add_argument('-m', '--testcase_remove_source_file', required=False, default='', help='(Optional) Testcase remove source file used to define pattern(s) for testcase to be removed')
    parser_build.add_argument('-f', '--force_create', required=False, default='False', help='Force create even when test result files already exist')
