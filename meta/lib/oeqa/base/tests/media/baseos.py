import unittest

class BaseOsTest(unittest.TestCase):
    '''Base os health check'''
    def test_baseos_dmesg(self):
        '''check dmesg command'''
        (status, output) = self.tc.target.run('dmesg')
        self.assertEqual(status, 0, msg="Error messages: %s" % output)

    def test_baseos_lsmod(self):
        '''check lsmod command'''
        (status, output) = self.tc.target.run('lsmod')
        self.assertEqual(status, 0, msg="Error messages: %s" % output)
