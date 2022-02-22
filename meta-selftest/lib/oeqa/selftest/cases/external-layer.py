from oeqa.selftest.case import OESelftestTestCase


class ImportedTests(OESelftestTestCase):

    def test_unconditional_pass(self):
        """
        Summary: Doesn't check anything, used to check import test from other layers.
        Expected: 1. Pass unconditionally
        Product: oe-core
        Author: Mariano Lopez <mariano.lopez@intel.com
        """

        self.assertEqual(True, True, msg = "Impossible to fail this test")
