import unittest

class TestSample(unittest.TestCase):
    def test_pass(self):
        """ Sample test, should pass """
        self.assertTrue(True, "test sample, always pass")
    def test_fail(self):
        """ Sample test, should fail """
        self.assertTrue(False, "test sample, always fails")

