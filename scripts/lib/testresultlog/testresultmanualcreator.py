import os
from testresultlog.testresultgitstore import TestResultGitStore

def main(args):
    if len(args.environment_list) > 0:
        env_list = args.environment_list.split(",")
    print(env_list)
    testresultstore = TestResultGitStore()
    testresultstore.create_manual_test_result(args.git_repo, args.git_branch, args.component, env_list, args.manual_tests_dir)

def register_commands(subparsers):
    """Register subcommands from this plugin"""
    parser_build = subparsers.add_parser('create_manual', help='Create test result for manual test result files',
                                         description='Create test result for manual test result files')
    parser_build.set_defaults(func=main)
    parser_build.add_argument('-c', '--component', required=True, help='Component to be selected from conf/testplan_component.conf for creation of test environments')
    parser_build.add_argument('-g', '--git_repo', required=False, default='default', help='(Optional) Git repository to be created, default will be <top_dir>/test-result-log-git')
    parser_build.add_argument('-b', '--git_branch', required=True, help='Git branch to be created for the git repository')
    parser_build.add_argument('-m', '--manual_tests_dir', required=True, help='Directory with manual test result files to be stored')
    parser_build.add_argument('-e', '--environment_list', required=False, default='', help='List of environment to be used to perform update')
