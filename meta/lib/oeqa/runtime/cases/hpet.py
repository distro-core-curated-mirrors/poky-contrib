from oeqa.runtime.case import OERuntimeTestCase

class HpetTest(OERuntimeTestCase):

    def test_hpet(self):
        (status, output) = self.target.run('cat /proc/timer_list | grep hpet')
        msg = 'status and output: %s and %s' % (status, output)
        self.assertEqual(status, 0, msg=msg)