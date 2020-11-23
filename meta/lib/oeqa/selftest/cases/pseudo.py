#
# SPDX-License-Identifier: MIT
#

from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import runCmd, bitbake, get_bb_var, get_bb_vars

class PseudoTest(OESelftestTestCase):
    # coreutils-native's cp can use pseudo to crash in some situations
    def test_coreutils_native(self):
        self.write_config('DEPENDS_pn-os-release = "coreutils-native"')
        bitbake("os-release -C unpack")
