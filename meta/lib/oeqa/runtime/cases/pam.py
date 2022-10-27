#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

# This test should cover https://bugzilla.yoctoproject.org/tr_show_case.cgi?case_id=287 testcase
# Note that the image under test must have "pam" in DISTRO_FEATURES

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.core.decorator.data import skipIfNotFeature
from oeqa.runtime.decorator.package import OEHasPackage

class PamBasicTest(OERuntimeTestCase):

    @skipIfNotFeature('pam', 'Test requires pam to be in DISTRO_FEATURES')
    @OETestDepends(['ssh.SSHTest.test_ssh'])
    @OEHasPackage(['shadow'])
    @OEHasPackage(['shadow-base'])
    def test_pam(self):
        status, output = self.target.run('login --help', ignore_status=True)
        msg = ('login command does not work as expected. '
               'Status and output:%s and %s' % (status, output))
        self.assertEqual(status, 1, msg = msg)

        self.target.run('passwd --help')

        self.target.run('su --help')

        self.target.run('useradd --help')
