import tempfile
import os
import pathlib
import json
import subprocess
import shutil
import scriptpath
scriptpath.add_bitbake_lib_path()
scriptpath.add_oe_lib_path()
from oeqa.utils.git import GitRepo, GitError

class TestResultGitStore(object):

    def __init__(self):
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.base_path = self.script_path + '/../../..'

    def _create_temporary_workspace_dir(self):
        return tempfile.mkdtemp(prefix='testresultlog.')

    def _remove_temporary_workspace_dir(self, workspace_dir):
        return subprocess.run(["rm", "-rf",  workspace_dir])

    def _get_project_environment_directory_path(self, project_dir, test_environment_list):
        project_env_dir = project_dir
        for env in test_environment_list:
            project_env_dir = os.path.join(project_env_dir, env)
        return project_env_dir

    def _get_testmodule_list(self, testmodule_testsuite_dict):
        return sorted(list(testmodule_testsuite_dict.keys()))

    def _get_testcase_list(self, testsuite_list, testsuite_testcase_dict):
        testcase_list = []
        for testsuite in sorted(testsuite_list):
            if testsuite in testsuite_testcase_dict:
                for testcase in testsuite_testcase_dict[testsuite]:
                    testcase_list.append(testcase)
        return testcase_list

    def _get_testcase_status(self, testcase, testcase_status_dict):
        if testcase in testcase_status_dict:
            return testcase_status_dict[testcase]
        return ""

    def _create_testcase_dict(self, testcase_list, testcase_status_dict):
        testcase_dict = {}
        for testcase in sorted(testcase_list):
            #testcase_key = '%s.%s' % (testsuite_name, testcase)
            testcase_status = self._get_testcase_status(testcase, testcase_status_dict)
            testcase_dict[testcase] = {"testresult": testcase_status,"bugs": ""}
        #print('DEBUG: testcase_dict: %s' % testcase_dict)
        return testcase_dict

    def _create_testsuite_testcase_teststatus_json_object(self, testsuite_list, testsuite_testcase_dict, testcase_status_dict):
        #print('DEBUG: creating testsuite testcase for testsuite list: %s' % testsuite_list)
        json_object = {'testsuite':{}}
        testsuite_dict = json_object['testsuite']
        for testsuite in sorted(testsuite_list):
            testsuite_dict[testsuite] = {'testcase': {}}
            #print('DEBUG: testsuite: %s' % testsuite)
            #print('DEBUG: testsuite_testcase_dict[testsuite]: %s' % testsuite_testcase_dict[testsuite])
            testsuite_dict[testsuite]['testcase'] = self._create_testcase_dict(testsuite_testcase_dict[testsuite], testcase_status_dict)
        return json_object

    def _create_testsuite_json_formatted_string(self, testsuite_list, testsuite_testcase_dict, testcase_status_dict):
        testsuite_testcase_list = self._create_testsuite_testcase_teststatus_json_object(testsuite_list, testsuite_testcase_dict, testcase_status_dict)
        return json.dumps(testsuite_testcase_list, sort_keys=True, indent=4)

    def _write_testsuite_testcase_json_formatted_string_to_file(self, file_path, file_content):
        with open(file_path, 'w') as the_file:
            the_file.write(file_content)

    def _write_log_file(self, file_path, logs):
        with open(file_path, 'w') as the_file:
            for line in logs:
                the_file.write(line + '\n')

    def _write_test_log_files(self, file_dir, testcase_list, testcase_logs_dict):
        for testcase in testcase_list:
            #print('testcase : %s' % testcase)
            if testcase in testcase_logs_dict:
                #print('testcase: %s' % testcase)
                #print('testcase logs: %s' % testcase_logs_dict[testcase])
                file_path = os.path.join(file_dir, '%s.log' % testcase)
                self._write_log_file(file_path, testcase_logs_dict[testcase])

    def _copy_files_from_source_to_destination_dir(self, source_dir, destination_dir):
        if os.path.exists(source_dir) and os.path.exists(destination_dir):
            for item in os.listdir(source_dir):
                s = os.path.join(source_dir, item)
                d = os.path.join(destination_dir, item)
                shutil.copy2(s, d)

    def _create_automated_test_result_from_empty_git(self, git_dir, git_branch, project, environment_list, testmodule_testsuite_dict, testsuite_testcase_dict, testcase_status_dict, testcase_logs_dict):
        workspace_dir = self._create_temporary_workspace_dir()
        project_dir = os.path.join(workspace_dir, project)
        project_env_dir = self._get_project_environment_directory_path(project_dir, environment_list)
        pathlib.Path(project_env_dir).mkdir(parents=True, exist_ok=True)
        for testmodule in self._get_testmodule_list(testmodule_testsuite_dict):
            testsuite_list = testmodule_testsuite_dict[testmodule]
            module_json_structure = self._create_testsuite_json_formatted_string(testsuite_list, testsuite_testcase_dict, testcase_status_dict)
            file_name = '%s.json' % testmodule
            file_path = os.path.join(project_env_dir, file_name)
            self._write_testsuite_testcase_json_formatted_string_to_file(file_path, module_json_structure)
            testcase_list = self._get_testcase_list(testsuite_list, testsuite_testcase_dict)
            self._write_test_log_files(project_env_dir, testcase_list, testcase_logs_dict)
        self._push_testsuite_testcase_json_file_to_git_repo(workspace_dir, git_dir, git_branch)
        self._remove_temporary_workspace_dir(workspace_dir)

    def _create_automated_test_result_from_existing_git(self, git_dir, git_branch, project, environment_list, testmodule_testsuite_dict, testsuite_testcase_dict, testcase_status_dict, testcase_logs_dict):
        project_dir = os.path.join(git_dir, project)
        project_env_dir = self._get_project_environment_directory_path(project_dir, environment_list)
        pathlib.Path(project_env_dir).mkdir(parents=True, exist_ok=True)
        for testmodule in self._get_testmodule_list(testmodule_testsuite_dict):
            testsuite_list = testmodule_testsuite_dict[testmodule]
            module_json_formatted_string = self._create_testsuite_json_formatted_string(testsuite_list, testsuite_testcase_dict, testcase_status_dict)
            file_name = '%s.json' % testmodule
            file_path = os.path.join(project_env_dir, file_name)
            self._write_testsuite_testcase_json_formatted_string_to_file(file_path, module_json_formatted_string)
            testcase_list = self._get_testcase_list(testsuite_list, testsuite_testcase_dict)
            self._write_test_log_files(project_env_dir, testcase_list, testcase_logs_dict)
        self._push_testsuite_testcase_json_file_to_git_repo(git_dir, git_dir, git_branch)

    def _create_manual_test_result_from_empty_git(self, git_dir, git_branch, project, environment_list, manual_test_report_dir):
        workspace_dir = self._create_temporary_workspace_dir()
        project_dir = os.path.join(workspace_dir, project)
        project_env_dir = self._get_project_environment_directory_path(project_dir, environment_list)
        pathlib.Path(project_env_dir).mkdir(parents=True, exist_ok=True)
        # cp files from manual_test_report_dir to project_env_dir
        # Not yet implement
        self._copy_files_from_source_to_destination_dir(manual_test_report_dir, project_env_dir)
        self._push_testsuite_testcase_json_file_to_git_repo(workspace_dir, git_dir, git_branch)
        self._remove_temporary_workspace_dir(workspace_dir)

    def _create_manual_test_result_from_exiting_git(self, git_dir, git_branch, project, environment_list, manual_test_report_dir):
        project_dir = os.path.join(git_dir, project)
        project_env_dir = self._get_project_environment_directory_path(project_dir, environment_list)
        if not self._check_if_git_dir_contain_project_and_environment_directory(git_dir, project, environment_list):
            pathlib.Path(project_env_dir).mkdir(parents=True, exist_ok=True)
        # cp files from manual_test_report_dir to existing project_env_dir
        # Not yet implement
        self._copy_files_from_source_to_destination_dir(manual_test_report_dir, project_env_dir)
        self._push_testsuite_testcase_json_file_to_git_repo(git_dir, git_dir, git_branch)

    def _load_test_module_file_with_json_into_dictionary(self, file):
        if os.path.exists(file):
            with open(file, "r") as f:
                return json.load(f)
        else:
            print('Cannot find file (%s)' % file)
            return None

    def _get_testcase_log_need_removal_list(self, testcase, cur_testcase_status, next_testcase_status, testcase_log_remove_list):
        if cur_testcase_status == 'FAILED' or cur_testcase_status == 'ERROR':
            if next_testcase_status == 'PASSED' or next_testcase_status == 'SKIPPED':
                testcase_log_remove_list.append(testcase)

    def _update_target_testresult_dictionary_with_status(self, target_testresult_dict, testsuite_list, testsuite_testcase_dict, testcase_status_dict, testcase_log_remove_list):
        for testsuite in testsuite_list:
            testcase_list = testsuite_testcase_dict[testsuite]
            for testcase in testcase_list:
                if testcase in testcase_status_dict:
                    cur_testcase_status = target_testresult_dict['testsuite'][testsuite]['testcase'][testcase]['testresult']
                    next_testcase_status = testcase_status_dict[testcase]
                    self._get_testcase_log_need_removal_list(testcase, cur_testcase_status, next_testcase_status, testcase_log_remove_list)
                    target_testresult_dict['testsuite'][testsuite]['testcase'][testcase]['testresult'] = next_testcase_status

    def _remove_test_log_files(self, file_dir, testcase_log_remove_list):
        for testcase_log_remove in testcase_log_remove_list:
            file_remove_path = os.path.join(file_dir, '%s.log' % testcase_log_remove)
            if os.path.exists(file_remove_path):
                os.remove(file_remove_path)

    def _check_if_git_dir_contain_project_and_environment_directory(self, git_dir, project, environment_list):
        project_dir = os.path.join(git_dir, project)
        project_env_dir = self._get_project_environment_directory_path(project_dir, environment_list)
        completed_process = subprocess.run(["ls", project_env_dir])
        if completed_process.returncode == 0:
            return True
        else:
            return False

    def _git_check_if_git_dir_and_git_branch_exist(self, git_dir, git_branch):
        completed_process = subprocess.run(["ls", '%s/.git' % git_dir])
        if not completed_process.returncode == 0:
            return False
        repo = self._git_init(git_dir)
        try:
            repo.run_cmd('checkout %s' % git_branch)
            return True
        except GitError:
            return False

    def _git_init(self, git_dir):
        try:
            repo = GitRepo(git_dir, is_topdir=True)
        except GitError:
            print("Non-empty directory that is not a Git repository "
                   "at {}\nPlease specify an existing Git repository, "
                   "an empty directory or a non-existing directory "
                   "path.".format(git_dir))
        return repo

    def _git_checkout_git_repo(self, repo, git_branch):
        repo.run_cmd('checkout %s' % git_branch)

    def _git_checkout_git_repo(self, repo, git_branch):
        repo.run_cmd('checkout %s' % git_branch)

    def _git_check_if_local_repo_contain_remote_origin(self, repo):
        try:
            repo.run_cmd('remote get-url origin')
            return True
        except GitError:
            return False

    def _git_check_if_local_repo_remote_origin_url_match(self, repo, git_remote):
        try:
            origin_url = repo.run_cmd('remote get-url origin')
            if origin_url == git_remote:
                return True
            else:
                return False
        except GitError:
            return False

    def _git_fetch_remote_origin(self, repo):
        print('Fetching remote origin to local repo')
        try:
            repo.run_cmd('fetch origin')
            return True
        except GitError:
            return False

    def _git_check_if_remote_origin_has_branch(self, repo, git_branch):
        try:
            output = repo.run_cmd('show-branch remotes/origin/%s' % git_branch)
            print(output)
            return True
        except GitError:
            return False

    def _git_add_local_repo_remote_origin(self, repo, git_remote):
        print('Adding remote origin to local repo')
        try:
            repo.run_cmd('remote add origin %s' % git_remote)
        except GitError:
            print("The remote add origin failed inside the Git repository")

    def _git_remove_local_repo_remote_origin(self, repo):
        print('Removing outdated remote origin from local repo')
        try:
            repo.run_cmd('remote remove origin')
        except GitError:
            print("The remote remove origin failed inside the Git repository")

    def _git_fetch_remote_origin_branch(self, repo, git_branch):
        print('Fetch remote origin %s' % git_branch)
        try:
            repo.run_cmd('fetch origin %s' % git_branch)
        except GitError:
            print("The fetch origin % failed inside the Git repository" % git_branch)

    def _git_rebase_remote_origin(self, repo, git_branch):
        print('Rebasing origin/%s' % git_branch)
        try:
            repo.run_cmd('rebase origin/%s' % git_branch)
        except GitError:
            print("The rebase origin/% failed inside the Git repository" % git_branch)

    def _git_push_local_branch_to_remote_origin(self, repo, git_branch):
        print('Pushing origin %s' % git_branch)
        try:
            repo.run_cmd('push origin %s' % git_branch)
        except GitError:
            print("The push origin % failed inside the Git repository" % git_branch)

    def _push_testsuite_testcase_json_file_to_git_repo(self, file_dir, git_repo, git_branch):
        return subprocess.run(["oe-git-archive", file_dir, "-g", git_repo, "-b", git_branch])

    def create_automated_test_result(self, git_dir, git_branch, project, environment_list, testmodule_testsuite_dict, testsuite_testcase_dict):
        print('Creating test result for environment list: %s' % environment_list)
        if self._git_check_if_git_dir_and_git_branch_exist(git_dir, git_branch):
            repo = self._git_init(git_dir)
            self._git_checkout_git_repo(repo, git_branch)
            print('Found git_dir and git_branch: %s %s' % (git_dir, git_branch))
            print('Entering git_dir: %s' % git_dir)
            if self._check_if_git_dir_contain_project_and_environment_directory(git_dir, project, environment_list):
                print('Found project and environment inside git_dir: %s' % git_dir)
                print('Since project and environment already exist, could not proceed to create.')
            else:
                print('Could not find project and environment inside git_dir: %s' % git_dir)
                print('Creating project and environment inside git_dir: %s' % git_dir)
                self._create_automated_test_result_from_existing_git(git_dir, git_branch, project, environment_list, testmodule_testsuite_dict, testsuite_testcase_dict, {}, {})
        else:
            print('Could not find git_dir or git_branch: %s %s' % (git_dir, git_branch))
            print('Creating git_dir, git_branch, project, and environment: %s' % git_dir)
            self._create_automated_test_result_from_empty_git(git_dir, git_branch, project, environment_list, testmodule_testsuite_dict, testsuite_testcase_dict, {}, {})

    def update_automated_test_result(self, git_dir, git_branch, project, environment_list, testmodule_testsuite_dict, testsuite_testcase_dict, testcase_status_dict, testcase_logs_dict):
        print('Updating test result for environment list: %s' % environment_list)
        repo = self._git_init(git_dir)
        self._git_checkout_git_repo(repo, git_branch)
        project_dir = os.path.join(git_dir, project)
        project_env_dir = self._get_project_environment_directory_path(project_dir, environment_list)
        testcase_log_remove_list = []
        for testmodule in self._get_testmodule_list(testmodule_testsuite_dict):
            testmodule_file = os.path.join(project_env_dir, '%s.json' % testmodule)
            target_testresult_dict = self._load_test_module_file_with_json_into_dictionary(testmodule_file)
            testsuite_list = testmodule_testsuite_dict[testmodule]
            self._update_target_testresult_dictionary_with_status(target_testresult_dict, testsuite_list, testsuite_testcase_dict, testcase_status_dict, testcase_log_remove_list)
            self._write_testsuite_testcase_json_formatted_string_to_file(testmodule_file, json.dumps(target_testresult_dict, sort_keys=True, indent=4))
            testcase_list = self._get_testcase_list(testsuite_list, testsuite_testcase_dict)
            self._write_test_log_files(project_env_dir, testcase_list, testcase_logs_dict)
        self._remove_test_log_files(project_env_dir, testcase_log_remove_list)
        self._push_testsuite_testcase_json_file_to_git_repo(git_dir, git_dir, git_branch)

    def smart_update_automated_test_result(self, git_dir, git_branch, project, environment_list, testmodule_testsuite_dict, testsuite_testcase_dict, testcase_status_dict, testcase_logs_dict):
        print('Creating/Updating test result for environment list: %s' % environment_list)
        if self._git_check_if_git_dir_and_git_branch_exist(git_dir, git_branch):
            repo = self._git_init(git_dir)
            self._git_checkout_git_repo(repo, git_branch)
            print('Found git_dir and git_branch: %s %s' % (git_dir, git_branch))
            print('Entering git_dir: %s' % git_dir)
            if self._check_if_git_dir_contain_project_and_environment_directory(git_dir, project, environment_list):
                print('Found project and environment inside git_dir: %s' % git_dir)
                print('Updating test result')
                self.update_automated_test_result(git_dir, git_branch, project, environment_list, testmodule_testsuite_dict, testsuite_testcase_dict, testcase_status_dict, testcase_logs_dict)
            else:
                print('Could not find project and environment inside git_dir: %s' % git_dir)
                print('Creating project and environment inside git_dir: %s' % git_dir)
                self._create_automated_test_result_from_existing_git(git_dir, git_branch, project, environment_list, testmodule_testsuite_dict, testsuite_testcase_dict, testcase_status_dict, testcase_logs_dict)
        else:
            print('Could not find git_dir or git_branch: %s %s' % (git_dir, git_branch))
            print('Creating git_dir, git_branch, project, and environment: %s' % git_dir)
            self._create_automated_test_result_from_empty_git(git_dir, git_branch, project, environment_list, testmodule_testsuite_dict, testsuite_testcase_dict, testcase_status_dict, testcase_logs_dict)

    def create_manual_test_result(self, git_dir, git_branch, project, environment_list, manual_test_report_dir):
        print('Creating test result for environment list: %s' % environment_list)
        if self._git_check_if_git_dir_and_git_branch_exist(git_dir, git_branch):
            repo = self._git_init(git_dir)
            self._git_checkout_git_repo(repo, git_branch)
            print('Found git_dir and git_branch: %s %s' % (git_dir, git_branch))
            print('Entering git_dir: %s' % git_dir)
            if self._check_if_git_dir_contain_project_and_environment_directory(git_dir, project, environment_list):
                print('Found project and environment inside git_dir: %s' % git_dir)
                print('Since project and environment already exist, could not proceed to create.')
            else:
                print('Could not find project and environment inside git_dir: %s' % git_dir)
                print('Creating project and environment inside git_dir: %s' % git_dir)
                self._create_manual_test_result_from_exiting_git(git_dir, git_branch, project, environment_list, manual_test_report_dir)
        else:
            print('Could not find git_dir or git_branch: %s %s' % (git_dir, git_branch))
            print('Creating git_dir, git_branch, project, and environment: %s' % git_dir)
            self._create_manual_test_result_from_empty_git(git_dir, git_branch, project, environment_list, manual_test_report_dir)

    def git_remote_fetch_rebase_push(self, git_dir, git_branch, git_remote):
        print('Pushing test result to remote git ...')
        repo = self._git_init(git_dir)
        print('Fetching, Rebasing, Pushing to remote')
        if self._git_check_if_local_repo_contain_remote_origin(repo):
            if not self._git_check_if_local_repo_remote_origin_url_match(repo, git_remote):
                self._git_remove_local_repo_remote_origin(repo)
                self._git_add_local_repo_remote_origin(repo, git_remote)
        else:
            self._git_add_local_repo_remote_origin(repo, git_remote)
        if self._git_fetch_remote_origin(repo):
            if self._git_check_if_remote_origin_has_branch(repo, git_branch):
                self._git_fetch_remote_origin_branch(repo, git_branch)
                self._git_rebase_remote_origin(repo, git_branch)
            self._git_push_local_branch_to_remote_origin(repo, git_branch)
        else:
            print('Git fetch origin failed. Stop proceeding to git push.')

    def checkout_git_branch(self, git_dir, git_branch):
        print('Checkout git branch ...')
        if self._git_check_if_git_dir_and_git_branch_exist(git_dir, git_branch):
            repo = self._git_init(git_dir)
            self._git_checkout_git_repo(repo, git_branch)
            return True
        else:
            print('Could not find git_dir or git_branch: %s %s' % (git_dir, git_branch))
            return False
