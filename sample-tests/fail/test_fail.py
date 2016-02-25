import unittest

class TestFail(unittest.TestCase):
    def test_fail(self):
        """ Sample test, should fail """
        self.assertTrue(False, "test sample, always fail")
