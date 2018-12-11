# test case management tool - store test result & log to git repository
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
import tempfile
import os
import subprocess
import shutil
import scriptpath
scriptpath.add_bitbake_lib_path()
scriptpath.add_oe_lib_path()
from oeqa.utils.git import GitRepo, GitError
from oe.path import copytree

class GitStore(object):

    def __init__(self, git_dir, git_branch):
        self.git_dir = git_dir
        self.git_branch = git_branch

    def _git_init(self):
        try:
            repo = GitRepo(self.git_dir, is_topdir=True)
        except GitError:
            raise GitError("Non-empty directory that is not a Git repository "
                           "at {}\nPlease specify an existing Git repository, "
                           "an empty directory or a non-existing directory "
                           "path.".format(self.git_dir))
        return repo

    def _run_git_cmd(self, repo, cmd):
        try:
            output = repo.run_cmd(cmd)
            return True, output
        except GitError:
            return False, None

    def check_if_git_dir_exist(self, logger):
        if not os.path.exists('%s/.git' % self.git_dir):
            logger.debug('Could not find destination git directory: %s' % self.git_dir)
            return False
        logger.debug('Found destination git directory: %s' % self.git_dir)
        return True

    def checkout_git_dir(self):
        repo = self._git_init()
        cmd = 'checkout %s' % self.git_branch
        return self._run_git_cmd(repo, cmd)

    def _check_if_need_sub_dir(self, logger, git_sub_dir):
        if len(git_sub_dir) > 0:
            logger.debug('Need to store into sub dir: %s' % git_sub_dir)
            return True
        logger.debug('No need to store into sub dir')
        return False

    def _check_if_sub_dir_exist(self, logger, git_sub_dir):
        if os.path.exists(os.path.join(self.git_dir, git_sub_dir)):
            logger.debug('Found existing sub directory: %s' % os.path.join(self.git_dir, git_sub_dir))
            return True
        logger.debug('Could not find existing sub directory: %s' % os.path.join(self.git_dir, git_sub_dir))
        return False

    def _check_if_testresults_file_exist(self, logger, file_name):
        if os.path.exists(os.path.join(self.git_dir, file_name)):
            logger.debug('Found existing %s file inside: %s' % (file_name, self.git_dir))
            return True
        logger.debug('Could not find %s file inside: %s' % (file_name, self.git_dir))
        return False

    def _check_if_need_overwrite_existing(self, logger, overwrite_result):
        if overwrite_result:
            logger.debug('Overwriting existing testresult')
        else:
            logger.debug('Skipped storing test result as it already exist. '
                         'Specify overwrite argument if you wish to delete existing testresult and store again.')
        return overwrite_result

    def _create_temporary_workspace_dir(self):
        return tempfile.mkdtemp(prefix='testresultlog.')

    def _remove_temporary_workspace_dir(self, workspace_dir):
        return subprocess.run(["rm", "-rf",  workspace_dir])

    def _make_directories(self, logger, target_dir):
        logger.debug('Creating directories: %s' % target_dir)
        bb.utils.mkdirhier(target_dir)

    def _copy_files(self, logger, source_dir, destination_dir):
        if os.path.exists(source_dir) and os.path.exists(destination_dir):
            logger.debug('Copying test result from %s to %s' % (source_dir, destination_dir))
            copytree(source_dir, destination_dir)

    def _get_commit_subject_and_body(self, git_sub_dir):
        commit_msg_subject = 'Store %s from {hostname}' % os.path.join(self.git_dir, git_sub_dir)
        commit_msg_body = 'git dir: %s\nsub dir list: %s\nhostname: {hostname}' % (self.git_dir, git_sub_dir)
        return commit_msg_subject, commit_msg_body

    def _store_files_to_git(self, logger, file_dir, commit_msg_subject, commit_msg_body):
        logger.debug('Storing test result into git repository (%s) and branch (%s)'
                     % (self.git_dir, self.git_branch))
        return subprocess.run(["oe-git-archive",
                               file_dir,
                               "-g", self.git_dir,
                               "-b", self.git_branch,
                               "--commit-msg-subject", commit_msg_subject,
                               "--commit-msg-body", commit_msg_body])

    def _store_files_to_new_git(self, logger, source_dir, git_sub_dir):
        logger.debug('Could not find destination git directory (%s) or git branch (%s)' %
                     (self.git_dir, self.git_branch))
        logger.debug('Storing files to new git')
        dest_top_dir = self._create_temporary_workspace_dir()
        dest_sub_dir = os.path.join(dest_top_dir, git_sub_dir)
        self._make_directories(logger, dest_sub_dir)
        self._copy_files(logger, source_dir, dest_sub_dir)
        commit_msg_subject, commit_msg_body = self._get_commit_subject_and_body(git_sub_dir)
        self._store_files_to_git(logger, dest_top_dir, commit_msg_subject, commit_msg_body)
        self._remove_temporary_workspace_dir(dest_top_dir)

    def _store_files_into_sub_dir_of_existing_git(self, logger, source_dir, git_sub_dir):
        logger.debug('Storing files to existing git with sub directory')
        dest_dir = os.path.join(self.git_dir, git_sub_dir)
        self._make_directories(logger, dest_dir)
        self._copy_files(logger, source_dir, dest_dir)
        commit_msg_subject, commit_msg_body = self._get_commit_subject_and_body(git_sub_dir)
        self._store_files_to_git(logger, self.git_dir, commit_msg_subject, commit_msg_body)

    def _store_files_into_existing_git(self, logger, source_dir):
        logger.debug('Storing files to existing git without sub directory')
        self._copy_files(logger, source_dir, self.git_dir)
        commit_msg_subject, commit_msg_body = self._get_commit_subject_and_body('')
        self._store_files_to_git(logger, self.git_dir, commit_msg_subject, commit_msg_body)

    def store_test_result(self, logger, source_dir, git_sub_dir, overwrite_result):
        if self.check_if_git_dir_exist(logger) and self.checkout_git_dir():
            if self._check_if_need_sub_dir(logger, git_sub_dir):
                if self._check_if_sub_dir_exist(logger, git_sub_dir):
                    if self._check_if_need_overwrite_existing(logger, overwrite_result):
                        shutil.rmtree(os.path.join(self.git_dir, git_sub_dir))
                        self._store_files_into_sub_dir_of_existing_git(logger, source_dir, git_sub_dir)
                else:
                    self._store_files_into_sub_dir_of_existing_git(logger, source_dir, git_sub_dir)
            else:
                if self._check_if_testresults_file_exist(logger, 'testresults.json'):
                    if self._check_if_need_overwrite_existing(logger, overwrite_result):
                        self._store_files_into_existing_git(logger, source_dir)
                else:
                    self._store_files_into_existing_git(logger, source_dir)
        else:
            self._store_files_to_new_git(logger, source_dir, git_sub_dir)
