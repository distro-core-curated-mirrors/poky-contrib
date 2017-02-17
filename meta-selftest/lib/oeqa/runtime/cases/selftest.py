from oeqa.utils.httpserver import HTTPService

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.runtime.cases.smart import SmartTest

class Selftest(OERuntimeTestCase):

    @OETestDepends(['ssh.SSHTest.test_ssh'])
    def test_install_package(self):
        """
        Summary: Check basic package installation functionality.
        Expected: 1. Before the test socat must be installed using scp.
                  2. After the test socat must be unistalled using ssh.
                     This can't be checked in this test.
        Product: oe-core
        Author: Mariano Lopez <mariano.lopez@intel.com>
        """

        (status, output) = self.target.run("socat -V")
        self.assertEqual(status, 0, msg="socat is not installed")

    @OETestDepends(['selftest.Selftest.test_install_package'])
    def test_verify_unistall(self):
        """
        Summary: Check basic package installation functionality.
        Expected: 1. test_install_package must unistall socat.
                     This test is just to verify that.
        Product: oe-core
        Author: Mariano Lopez <mariano.lopez@intel.com>
        """

        (status, output) = self.target.run("socat -V")
        self.assertNotEqual(status, 0, msg="socat is still installed")

class SmartSelftest(SmartTest):

    @classmethod
    def setUpClass(cls):
        cls.repolist = []
        cls.repo_server = HTTPService(os.path.join(cls.tc.td['WORKDIR'], 'rpms'),
                                      cls.tc.target.server_ip)
        cls.repo_server.port = 8080
        cls.repo_server.start()

    @classmethod
    def tearDownClass(cls):
        cls.repo_server.stop()
        for repo in cls.repolist:
            cls.tc.target.run('smart channel -y --remove %s' % repo)

    @OETestDepends(['ssh.SSHTest.test_ssh'])
    def test_verify_package_feeds(self):
        """
        Summary: Check correct setting of PACKAGE_FEED_URIS var
        Expected: 1. Feeds were correctly set for smart
                  2. Update recovers packages from host's repo
        Author: Humberto Ibarra <humberto.ibarra.lopez@intel.com>
        """
        output = self.smart('update')
        import re
        new_pkgs = re.match(r".*Channels have [0-9]+ new packages", output, re.DOTALL)
        self.assertTrue(new_pkgs is not None, msg = "couldn't update packages")
