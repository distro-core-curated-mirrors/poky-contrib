from testresultlog.gitstore import GitStore

def main(args):
    if len(args.environment_list) > 0:
        env_list = args.environment_list.split(",")
    gitstore = GitStore()
    gitstore.create_manual_test_result(args.git_repo, args.git_branch, args.component, env_list, args.manual_tests_dir)
    return 0

def register_commands(subparsers):
    """Register subcommands from this plugin"""
    parser_build = subparsers.add_parser('store-manual', help='Store manual test status & log from manual-test-helper into git repository',
                                         description='Store manual test status & log from manual-test-helper into git repository',
                                         group='store')
    parser_build.set_defaults(func=main)
    parser_build.add_argument('component', help='Component folder (as the top folder) to store the test status & log')
    parser_build.add_argument('git_branch', help='Git branch to store the test status & log')
    parser_build.add_argument('manual_tests_dir', help='Directory with manual test result files from manual-test-helper to be stored')
    parser_build.add_argument('-g', '--git_repo', default='default', help='(Optional) Git repository used for storage, default will be <top_dir>/test-result-log.git')
    parser_build.add_argument('-e', '--environment_list', default='default', help='(Optional) List of environment seperated by comma (",") used to label the test environments for the stored test status & log')
