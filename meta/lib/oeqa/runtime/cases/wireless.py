from oeqa.runtime.case import OERuntimeTestCase

class WirelessTest(OERuntimeTestCase):

    def test_wireless(self):
        (status, output) = self.target.run('lspci -v | grep iwlwifi OR dmesg | grep iwlwifi OR lsmod | grep iwlwifi')
        msg = 'status and output: %s and %s' % (status, output)
        self.assertEqual(status, 0, msg=msg)