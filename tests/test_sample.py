from base import PatchTestBase

class TestSample(PatchTestBase):

    def test_all_pass(self):
        """ Sample test ALL pass"""
        a,b = 1,2
        self.assertEqual(a,a)
        self.assertNotEqual(a,b)
        self.assertTrue(True)
        self.assertFalse(False)

    def test_all_fail(self):
        """ Sample test ALL fail"""
        a,b = 1,2
        self.assertEqual(a,b)
        self.assertNotEqual(a,a)
        self.assertTrue(False)
        self.assertFalse(True)
