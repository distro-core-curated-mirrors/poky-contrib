import os
import unittest
from patchtestdata import PatchTestInput as pti

class TestRepository(unittest.TestCase):
    def test_repo_existence(self):
        """ Test existence of the repository folder """
        self.assertTrue(os.path.isdir(pti.repodir), 'repository directory does not exist')

    def test_git_repo(self):
        """ Test existence of of the .git folder """
        git_folder = os.path.join(pti.repodir, '.git')
        self.assertTrue(os.path.isdir(git_folder), 'The repository (%s) is not a git repo' % git_folder)

    def test_git_config(self):
        """ Test existence of the git configuration file """
        git_config = os.path.join(pti.repodir, '.git', 'config')
        self.assertTrue(os.path.isfile(git_config), 'The repository does not contain patchwork configuration data')

