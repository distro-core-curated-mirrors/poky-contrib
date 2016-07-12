from oeqa.selftest.base import oeSelfTest
from oeqa.utils.decorators import testcase

class ImportedTests(oeSelfTest):

    def test_unconditional_pass(self):
        """
        Summary: Doesn't check anything, used to check import test from other layers.
        Expected: 1. Pass unconditionally
        Product: oe-core
        Author: Mariano Lopez <mariano.lopez@intel.comr
        """

        self.assertEqual(True, True, msg = "Impossible to fail this test")
