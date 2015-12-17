import os
import unittest
from repo import Repo, RepoException

class PatchTestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Get the series and prepared repository"""

        cls.repo = Repo(cls.series, cls.revision,
                        cls.pw_url, cls.pw_project,
                        cls.pw_user, cls.pw_pass,
                        cls.repo_dir, cls.temp_base_dir,
                        cls.remote, cls.stable_branch)

        try:
            cls.repo.create()
            cls.repo.config()
            cls.repo.fetch()
            cls.repo.branch()
            cls.repo.patch()
        except RepoException:
            # catch the exception, so we clean the repository
            cls.repo.clean(remove_branch=True)

    @classmethod
    def tearDownClass(cls):
        cls.repo.clean()
