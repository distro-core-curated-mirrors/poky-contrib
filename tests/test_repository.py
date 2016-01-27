import os
import unittest
from patchtestargs import PatchTestArgs as pta

class TestRepository(unittest.TestCase):
    def test_repo_existance(self):
        """ Test existance of the repository folder """
        self.assertTrue(os.path.isdir(pta.repodir), 'repository directory does not exist')

    def test_git_repo(self):
        """ Test existance of of the .git folder """
        git_folder = os.path.join(pta.repodir, '.git')
        self.assertTrue(os.path.isdir(git_folder), 'The repository (%s) is not a git repo' % git_folder)

    def test_git_config(self):
        """ Test existance of the git configuration file """
        git_config = os.path.join(pta.repodir, '.git', 'config')
        self.assertTrue(os.path.isfile(git_config), 'The repository does not contain patchwork configuration data')

