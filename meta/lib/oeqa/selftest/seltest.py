from oeqa.selftest.base import oeSelfTest
from oeqa.utils.commands import runCmd
from oeqa.utils.decorators import testcase

class Selftest(oeSelfTest):

    def test_import_test_from_layer(self):
        """
        Summary: Checks functionality to import tests from other layers.
        Expected: 1. Must show "test_import_dummy" in the test list.
        Product: oe-core
        Author: Mariano Lopez <mariano.lopez@intel.com>
        """

        test_name = "imported.ImportedTests.test_import_dummy"
        error_msg = "Couldn't find test: %s; Not importing tests from other layers" % test_name
        result = runCmd("oe-selftest --list-tests")
        success = True if test_name in result.output else False
        self.assertEqual(success, True, msg = error_msg)
