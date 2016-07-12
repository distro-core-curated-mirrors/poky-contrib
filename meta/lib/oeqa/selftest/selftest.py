from oeqa.selftest.base import oeSelfTest
from oeqa.utils.commands import runCmd
from oeqa.utils.decorators import testcase

class ExternalLayer(oeSelfTest):

    def test_list_imported(self):
        """
        Summary: Checks functionality to import tests from other layers.
        Expected: 1. Must show "test_import_dummy" in the test list.
        Product: oe-core
        Author: Mariano Lopez <mariano.lopez@intel.com>
        """

        test_name = "external-layer.ImportedTests.test_unconditional_pass"
        error_msg = "Couldn't find test: %s; Not importing tests from other layers" % test_name
        result = runCmd("oe-selftest --list-tests")
        success = True if test_name in result.output else False
        self.assertEqual(success, True, msg = error_msg)
