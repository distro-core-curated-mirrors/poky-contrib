from oeqa.runtime.case import OERuntimeTestCase

class PcieTest(OERuntimeTestCase):

    def test_pcie(self):
        (status, output) = self.target.run('dmesg | grep pcie OR lspci -v | grep pcie')
        msg = 'status and output: %s and %s' % (status, output)
        self.assertEqual(status, 0, msg=msg)