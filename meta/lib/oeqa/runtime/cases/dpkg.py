import os
import re
import subprocess

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.core.decorator.oeid import OETestID
from oeqa.core.decorator.data import skipIfNotDataVar, skipIfNotFeature
from oeqa.runtime.decorator.package import OEHasPackage


class dpkgTest(OERuntimeTestCase):
    def dpkg(self, command, expectedStr, expected=0):
        status, output = self.target.run(command, 1500)
        message = os.linesep.join([command, output])
        self.assertIn(expectedStr, output) 
        self.assertEqual(status, expected, message)
        return output

class dpkgBasicTest(dpkgTest):
    @skipIfNotFeature('package-management','Test requires package-management to be in IMAGE_FEATURES')
    @skipIfNotDataVar('IMAGE_PKGTYPE','deb','DEB is not the primary package manager')
    @OEHasPackage(['dpkg'])
    
    @OETestDepends(['ssh.SSHTest.test_ssh'])
    @OETestID(1801)
    def test_dpkg_help(self):
        self.dpkg('dpkg --help',"Usage: dpkg [<option> ...] <command>")

    @OETestDepends(['dpkg.dpkgBasicTest.test_dpkg_help'])
    @OETestID(1802)
    def test_dpkg_version(self):
        self.dpkg('dpkg --version',"Debian 'dpkg' package management program version")

    @OETestID(1803)
    def test_dpkg_Dhelp(self):
        self.dpkg('dpkg -Dhelp',"dpkg debugging option, --debug=<octal> or -D<octal>:")

    @OETestID(1805)
    def test_dpkg_force_help(self):
        self.dpkg('dpkg --force-help',"dpkg forcing options - control behaviour when problems found:")

    @OETestID(1806)
    def test_dpkg_deb_help(self):
        self.dpkg('dpkg-deb --help',"Usage: dpkg-deb [<option> ...] <command>")

    @OETestID(1812)
    def test_dpkg_status(self):
        self.dpkg('dpkg -s dpkg',"Package: dpkg")

    @OETestID(1814)
    def test_dpkg_list(self):
        self.dpkg('dpkg -l',"Desired=Unknown/Install/Remove/Purge/Hold")
