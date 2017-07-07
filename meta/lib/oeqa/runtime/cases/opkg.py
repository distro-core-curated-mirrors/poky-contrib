import os
import re
import subprocess

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.core.decorator.oeid import OETestID
from oeqa.core.decorator.data import skipIfNotDataVar, skipIfNotFeature
from oeqa.runtime.decorator.package import OEHasPackage

class opkgTest(OERuntimeTestCase):
    def opkg(self, command, expected = 0):
        command = 'opkg %s' % command
        status, output = self.target.run(command, 1500)
        message = os.linesep.join([command, output])
        self.assertEqual(status, expected, message)
        return output

class opkgBasicTest(opkgTest):
    @skipIfNotFeature('package-management', 'Test requires package-management to be in IMAGE_FEATURES')
    @skipIfNotDataVar('IMAGE_PKGTYPE','ipk', 'IPK is not the primary package manager')
    @OEHasPackage(['opkg'])

    @OETestDepends(['ssh.SSHTest.test_ssh'])
    @OETestID(1841)
    def test_opkg_list(self):
       self.opkg('list')

    @OETestID(1842)
    def test_opkg_list_installed(self):
       self.opkg('list-installed')

    @OETestID(1843)
    def test_opkg_depends(self):
       self.opkg('depends opkg')

    @OETestID(1837)
    def test_opkg_whatdepends(self):
      self.opkg('whatdepends opkg')

    @OETestID(1838)
    def test_opkg_status(self):
      self.opkg('status')

    @OETestID(1839)
    def test_opkg_info(self):
        self.opkg('info opkg')

    @OETestID(1840)
    def test_opkg_print_architecture(self):
        self.opkg('print-architecture')
