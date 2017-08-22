from oeqa.selftest.case import OESelftestTestCase
from oeqa.core.decorator.oeid import OETestID
import tempfile

class TestImage(OESelftestTestCase):
    _use_own_builddir = True
    _main_thread = False

    @OETestID(1644)
    def test_testimage_install(self):
        """
        Summary: Check install packages functionality for testimage/testexport.
        Expected: 1. Import tests from a directory other than meta.
                  2. Check install/uninstall of socat.
        Product: oe-core
        Author: Mariano Lopez <mariano.lopez@intel.com>
        """
        if self.get_bb_var('DISTRO') == 'poky-tiny':
            self.skipTest('core-image-full-cmdline not buildable for poky-tiny')

        features = 'INHERIT += "testimage"\n'
        features += 'TEST_SUITES = "ping ssh selftest"\n'
        self.write_config(features)

        # Build core-image-sato and testimage
        self.bitbake('core-image-full-cmdline socat')
        self.bitbake('-c testimage core-image-full-cmdline')

    @OETestID(1883)
    def test_testimage_dnf(self):
        """
        Summary: Check package feeds functionality for dnf
        Expected: 1. Check that remote package feeds can be accessed
        Product: oe-core
        Author: Alexander Kanavin <alexander.kanavin@intel.com>
        """
        if self.get_bb_var('DISTRO') == 'poky-tiny':
            self.skipTest('core-image-full-cmdline not buildable for poky-tiny')

        features = 'INHERIT += "testimage"\n'
        features += 'TEST_SUITES = "ping ssh dnf_runtime dnf.DnfBasicTest.test_dnf_help"\n'
        # We don't yet know what the server ip and port will be - they will be patched
        # in at the start of the on-image test
        features += 'PACKAGE_FEED_URIS = "http://bogus_ip:bogus_port"\n'
        features += 'EXTRA_IMAGE_FEATURES += "package-management"\n'
        features += 'PACKAGE_CLASSES = "package_rpm"\n'

        # Enable package feed signing
        self.gpg_home = tempfile.TemporaryDirectory(prefix="oeqa-feed-sign-")
        signing_key_dir = os.path.join(self.testlayer_path, 'files', 'signing')
        self.runCmd('gpg --batch --homedir %s --import %s' % (self.gpg_home.name, os.path.join(signing_key_dir, 'key.secret')))
        features += 'INHERIT += "sign_package_feed"\n'
        features += 'PACKAGE_FEED_GPG_NAME = "testuser"\n'
        features += 'PACKAGE_FEED_GPG_PASSPHRASE_FILE = "%s"\n' % os.path.join(signing_key_dir, 'key.passphrase')
        features += 'GPG_PATH = "%s"\n' % self.gpg_home.name
        self.write_config(features)

        # Build core-image-sato and testimage
        self.bitbake('core-image-full-cmdline socat')
        self.bitbake('-c testimage core-image-full-cmdline')
