#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake

class PicolibcTest(OESelftestTestCase):
    def test_picolibc(self):
        self.write_config('TCLIBC = "picolibc"')
        bitbake("picolibc-helloworld")
