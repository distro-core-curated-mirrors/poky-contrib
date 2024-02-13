#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import get_bb_var, get_bb_vars, bitbake, runCmd
import oe.path
import os

class LibOE(OESelftestTestCase):

    @classmethod
    def setUpClass(cls):
        super(LibOE, cls).setUpClass()
        cls.tmp_dir = get_bb_var('TMPDIR')

    def test_copy_tree_special(self):
        """
        Summary:    oe.path.copytree() should copy files with special character
        Expected:   'test file with sp£c!al @nd spaces' should exist in
                    copy destination
        Product:    OE-Core
        Author:     Joshua Lock <joshua.g.lock@intel.com>
        """
        testloc = oe.path.join(self.tmp_dir, 'liboetests')
        src = oe.path.join(testloc, 'src')
        dst = oe.path.join(testloc, 'dst')
        bb.utils.mkdirhier(testloc)
        bb.utils.mkdirhier(src)
        testfilename = 'test file with sp£c!al @nd spaces'

        # create the test file and copy it
        open(oe.path.join(src, testfilename), 'w+b').close()
        oe.path.copytree(src, dst)

        # ensure path exists in dest
        fileindst = os.path.isfile(oe.path.join(dst, testfilename))
        self.assertTrue(fileindst, "File with spaces doesn't exist in dst")

        oe.path.remove(testloc)

    def test_copy_tree_xattr(self):
        """
        Summary:    oe.path.copytree() should preserve xattr on copied files
        Expected:   testxattr file in destination should have user.oetest
                    extended attribute
        Product:    OE-Core
        Author:     Joshua Lock <joshua.g.lock@intel.com>
        """
        testloc = oe.path.join(self.tmp_dir, 'liboetests')
        src = oe.path.join(testloc, 'src')
        dst = oe.path.join(testloc, 'dst')
        bb.utils.mkdirhier(testloc)
        bb.utils.mkdirhier(src)
        testfilename = 'testxattr'

        # ensure we have setfattr available
        bitbake("attr-native")

        bb_vars = get_bb_vars(['SYSROOT_DESTDIR', 'bindir'], 'attr-native')
        destdir = bb_vars['SYSROOT_DESTDIR']
        bindir = bb_vars['bindir']
        bindir = destdir + bindir

        # create a file with xattr and copy it
        open(oe.path.join(src, testfilename), 'w+b').close()
        runCmd('%s/setfattr -n user.oetest -v "testing liboe" %s' % (bindir, oe.path.join(src, testfilename)))
        oe.path.copytree(src, dst)

        # ensure file in dest has user.oetest xattr
        result = runCmd('%s/getfattr -n user.oetest %s' % (bindir, oe.path.join(dst, testfilename)))
        self.assertIn('user.oetest="testing liboe"', result.output, 'Extended attribute not sert in dst')

        oe.path.remove(testloc)

    def test_copy_hardlink_tree_count(self):
        """
        Summary:    oe.path.copyhardlinktree() shouldn't miss out files
        Expected:   src and dst should have the same number of files
        Product:    OE-Core
        Author:     Joshua Lock <joshua.g.lock@intel.com>
        """
        testloc = oe.path.join(self.tmp_dir, 'liboetests')
        src = oe.path.join(testloc, 'src')
        dst = oe.path.join(testloc, 'dst')
        bb.utils.mkdirhier(testloc)
        bb.utils.mkdirhier(src)
        testfiles = ['foo', 'bar', '.baz', 'quux']

        def touchfile(tf):
            open(oe.path.join(src, tf), 'w+b').close()

        for f in testfiles:
            touchfile(f)

        oe.path.copyhardlinktree(src, dst)

        dstcnt = len(os.listdir(dst))
        srccnt = len(os.listdir(src))
        self.assertEqual(dstcnt, len(testfiles), "Number of files in dst (%s) differs from number of files in src(%s)." % (dstcnt, srccnt))

        oe.path.remove(testloc)

    def test_distro_features_filter(self):
        config = """
# Nuke any distro-level manipulation of the features
DISTRO = "nodistro"
INIT_MANAGER = "none"
VIRTUAL-RUNTIME_init_manager = ""

# The base features
DISTRO_FEATURES = "a b c d"

# The base features get filtered through this mask
DISTRO_FEATURES_FILTER_NATIVE = "a c"
DISTRO_FEATURES_FILTER_NATIVESDK = "b d"
# TODO consider backfill?

# These features are always enabled
DISTRO_FEATURES_NATIVE = "f"
DISTRO_FEATURES_NATIVESDK = "g"

DISTRO_FEATURES_BACKFILL:forcevariable = "e"
        """
        self.write_config(config)

        def features(expected, recipe):
            calculated = set(get_bb_var("DISTRO_FEATURES", recipe).split())
            self.assertEqual(set(expected), calculated, "FEATURE mismatch for %s" % recipe)
        
        features("abcde", "m4")
        features("acf", "m4-native")
        features("bdg", "nativesdk-m4")

        # TODO machine features
