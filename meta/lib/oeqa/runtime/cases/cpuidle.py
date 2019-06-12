from oeqa.runtime.case import OERuntimeTestCase

class CpuidleTest(OERuntimeTestCase):

    def test_cpu_idle(self):
        (status, output) = self.target.run('cat /sys/devices/system/cpu/cpuidle/current_driver')
        msg = 'status and output: %s and %s' % (status, output)
        self.assertEqual(status, 0, msg=msg)