import os
import sys
import shutil
import unittest

from glob import glob

from oeqa.sdkext.case import OESDKExtTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.core.decorator.oeid import OETestID
from oeqa.utils.commands import runCmd


class WicTest(OESDKExtTestCase):
    """Wic test within eSDK."""

    testdir = "/var/tmp/wic.test.sdkext/"
    outfile = "/var/tmp/wic.test.sdkext/output.txt"

    @OETestID(1963)
    def test_wic_location(self):
        """Check whether wic is run within eSDK sysroot"""
        output = self._run("which wic")
        self.assertEqual(output.startswith(self.tc.sdk_dir), True, \
            msg="Seems that wic isn't the eSDK one : %s" % output)

    def _exec_wic_cmd(self, cmd):
        """Wrapper to execute wic command and check status"""
        status = runCmd("cd %s; . %s; %s" % (self.tc.sdk_dir, self.tc.sdk_env, cmd)).status
        self.assertEqual(0, status)

    def _exec_devtool_build(self):
        """Wrapper to build image as pre-requisite for wic"""
        cmd = "devtool build-image"
        runCmd("cd %s; . %s; %s" % (self.tc.sdk_dir, self.tc.sdk_env, cmd))

    def _get_img_type(self):
        """Wrapper to get SDK target for image creation"""
        # Get sdk_targets from devtool.conf
        conf_file = self.tc.sdk_dir + "conf/devtool.conf"
        with open (conf_file, 'r') as in_file:
             for line in in_file:
                if 'sdk_targets' in line:
                    image = line.split()
                    for img_name in image:
                        if img_name.startswith('core-image'):
                            break
        return img_name

    def _get_line_count(self):
        count = 0
        with open (self.outfile, 'r') as output:
            count = sum(1 for line in output if line.rstrip('\n'))
        return count

    @OETestID(1964)
    @OETestDepends(['test_wic_location'])
    def test_wic_version(self):
        cmd = "wic --version"
        self._exec_wic_cmd(cmd)

    @OETestID(1965)
    @OETestDepends(['test_wic_location'])
    def test_wic_help(self):
        cmd = "wic --help"
        self._exec_wic_cmd(cmd)
        cmd = "wic -h"
        self._exec_wic_cmd(cmd)

    @OETestID(1966)
    @OETestDepends(['test_wic_location'])
    def test_wic_create_help(self):
        cmd = "wic create --help"
        self._exec_wic_cmd(cmd)

    @OETestID(1967)
    @OETestDepends(['test_wic_location'])
    def test_wic_list_help(self):
        cmd = "wic list --help"
        self._exec_wic_cmd(cmd)

    @OETestID(1968)
    @OETestDepends(['test_wic_location'])
    def test_wic_help_create(self):
        cmd = "wic help create"
        self._exec_wic_cmd(cmd)

    @OETestID(1969)
    @OETestDepends(['test_wic_location'])
    def test_wic_help_list(self):
        cmd = "wic help list"
        self._exec_wic_cmd(cmd)

    @OETestID(1970)
    @OETestDepends(['test_wic_location'])
    def test_wic_help_overview(self):
        cmd = "wic help overview"
        self._exec_wic_cmd(cmd)

    @OETestID(1971)
    @OETestDepends(['test_wic_location'])
    def test_wic_help_plugins(self):
        cmd = "wic help plugins"
        self._exec_wic_cmd(cmd)

    @OETestID(1972)
    @OETestDepends(['test_wic_location'])
    def test_wic_help_kickstart(self):
        cmd = "wic help kickstart"
        self._exec_wic_cmd(cmd)

    @OETestID(1973)
    @OETestDepends(['test_wic_location'])
    def test_wic_list_images(self):
        cmd = "wic list images"
        self._exec_wic_cmd(cmd)

    @OETestID(1974)
    @OETestDepends(['test_wic_location'])
    def test_wic_list_src_plugins(self):
        cmd = "wic list source-plugins"
        self._exec_wic_cmd(cmd)

    @OETestID(1976)
    @OETestDepends(['test_wic_location'])
    def test_wic_listed_images_help(self):
        cmd = "wic list images"
        output = runCmd("cd %s; %s" % (self.tc.sdk_dir, cmd)).output
        imagelist = [line.split()[0] for line in output.splitlines()]
        for img in imagelist:
            cmd = "wic list %s help" % img
            self._exec_wic_cmd(cmd)

    @OETestID(1977)
    @OETestDepends(['test_wic_location'])
    def test_wic_unsupported_subcommand(self):
        self.assertNotEqual(0, runCmd('wic unsupported', ignore_status=True).status)

    @OETestID(1978)
    @OETestDepends(['test_wic_location'])
    def test_wic_no_subcommand(self):
        self.assertEqual(1, runCmd('wic', ignore_status=True).status)

    @OETestID(1979)
    @OETestDepends(['test_wic_location'])
    def test_wic_mkefidisk_image(self):
        self._exec_devtool_build()
        image = self._get_img_type()
        cmd = "wic create mkefidisk --image-name %s -o %s" % (image, self.testdir)
        self._exec_wic_cmd(cmd)
        self.assertEqual(1, len(glob(self.testdir + "mkefidisk-*.direct")))

    @OETestID(1980)
    @OETestDepends(['test_wic_location', 'test_wic_mkefidisk_image'])
    def test_wic_ls(self):
        images = glob(self.testdir + "mkefidisk-*.direct")
        self.assertEqual(1, len(images))

        # list partition
        cmd = "wic ls %s > %s" % (images[0], self.outfile)
        self._exec_wic_cmd(cmd)
        count = self._get_line_count()
        self.assertEqual(4, count)

        # list directory content of the first partition
        cmd = "wic ls %s:1 > %s" % (images[0], self.outfile)
        self._exec_wic_cmd(cmd)
        count = self._get_line_count()
        self.assertEqual(7, count)
        # clean up testdir
        shutil.rmtree(self.testdir)
