import os
import unittest
from repo import Repo, PatchException

class PatchTestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Get the series and prepared repository"""

        cls.repo = Repo(cls.series, cls.revision,
                        cls.repodir, cls.tempbasedir)

        # TODO: cleaning the repo should not be neccessary because
        # the tearDownClass is doing it, but when the tests are 
        # interrupted, the repo may remain dirty. We should handle
        # the control+c correctly
        cls.repo.clean()
        cls.repo.fetch()
        cls.repo.branch()

        try:
            cls.repo.patch()
        except PatchException as pe:
            # catch the exception, so we clean the repository
            cls.repo.clean(removebranch=True)
            raise pe

    @classmethod
    def tearDownClass(cls):
        cls.repo.clean()
