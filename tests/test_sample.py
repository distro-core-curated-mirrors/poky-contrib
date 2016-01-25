import unittest
from patchtestargs import PatchTestArgs as pta

class TestSample(unittest.TestCase):
    def test_sample(self):
        self.assertTrue(pta.repodir)


