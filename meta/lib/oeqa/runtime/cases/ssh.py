#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.runtime.decorator.package import OEHasPackage

class SSHTest(OERuntimeTestCase):

    @OETestDepends(['ping.PingTest.test_ping'])
    @OEHasPackage(['dropbear', 'openssh-sshd'])
    def test_ssh(self):
        self.target.run('uname -a')
        # Check that controllerimage doesn't exist
        self.target.run('test ! -f /etc/controllerimage')
