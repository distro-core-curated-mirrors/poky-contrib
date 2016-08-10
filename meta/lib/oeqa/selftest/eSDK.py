import unittest
import tempfile
import shutil
import os
import glob
import logging
import subprocess
import oeqa.utils.ftools as ftools
from oeqa.utils.decorators import testcase 
from oeqa.selftest.base import oeSelfTest
from oeqa.utils.commands import runCmd, bitbake, get_bb_var
from oeqa.utils.httpserver import HTTPService

class oeSDKExtSelfTest(oeSelfTest):
    """
    # Bugzilla Test Plan: 6033
    # This code is planned to be part of the automation for eSDK containig
    # Install libraries and headers, image generation binary feeds, Node.js Installation, Node.js test recipes 
    # and sdk update devtool.
    """

    @staticmethod
    def get_esdk_environment(env_eSDK, tmpdir_eSDKQA):
        # XXX: at this time use the first env need to investigate
        # what environment load oe-selftest, i586, x86_64
        pattern = os.path.join(tmpdir_eSDKQA, 'environment-setup-*')
        return glob.glob(pattern)[0]
    
    @staticmethod
    def run_esdk_cmd(env_eSDK, tmpdir_eSDKQA, cmd, postconfig=None, **options):
        if postconfig:
            esdk_conf_file = os.path.join(tmpdir_eSDKQA, 'conf', 'local.conf')
            with open(esdk_conf_file, 'a+') as f:
                f.write(postconfig)
        if not options:
            options = {}
        if not 'shell' in options:
            options['shell'] = True

        runCmd("cd %s; . %s; %s" % (tmpdir_eSDKQA, env_eSDK, cmd), **options)

    @staticmethod
    def generate_eSDK(image):
        pn_task = '%s -c populate_sdk_ext' % image
        bitbake(pn_task)

    @staticmethod
    def get_eSDK_toolchain(image):
        pn_task = '%s -c populate_sdk_ext' % image

        sdk_deploy = get_bb_var('SDK_DEPLOY', pn_task)
        toolchain_name = get_bb_var('TOOLCHAINEXT_OUTPUTNAME', pn_task)
        return os.path.join(sdk_deploy, toolchain_name + '.sh')
    

    @classmethod
    def setUpClass(cls):
        # Start to serve sstate dir
        sstate_dir = os.path.join(os.environ['BUILDDIR'], 'sstate-cache')
        cls.http_service = HTTPService(sstate_dir)
        cls.http_service.start()

        http_url = "localhost:%d" % cls.http_service.port
 
        image = 'core-image-minimal'

        cls.tmpdir_eSDKQA = tempfile.mkdtemp(prefix='eSDKQA')
        oeSDKExtSelfTest.generate_eSDK(image)

        # Install eSDK
        ext_sdk_path = oeSDKExtSelfTest.get_eSDK_toolchain(image)
        runCmd("%s -y -d \"%s\"" % (ext_sdk_path, cls.tmpdir_eSDKQA))

        cls.env_eSDK = oeSDKExtSelfTest.get_esdk_environment('', cls.tmpdir_eSDKQA)

        # Configure eSDK to use sstate mirror from poky
        sstate_config="""
SDK_LOCAL_CONF_WHITELIST = "SSTATE_MIRRORS"
SSTATE_MIRRORS =  "file://.* http://%s/PATH"
        """ % http_url
        with open(os.path.join(cls.tmpdir_eSDKQA, 'conf', 'local.conf'), 'a+') as f:
            f.write(sstate_config)

        # Common variables
        cls.package_nodejs = "npm://registry.npmjs.org;name=forever;version=0.15.1"
      
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmpdir_eSDKQA)
        cls.http_service.stop()

    @testcase (1471)
    def test_Install_Libraries_Headers(self):
        pn_sstate = 'bc'
        bitbake(pn_sstate)
        cmd = "devtool sdk-install %s " % pn_sstate
        oeSDKExtSelfTest.run_esdk_cmd(self.env_eSDK, self.tmpdir_eSDKQA, cmd)
    
    @testcase(1472)
    def test_Image_Generation_binary_feeds(self):
        image = 'core-image-minimal'
        cmd = "devtool build-image %s" % image
        oeSDKExtSelfTest.run_esdk_cmd(self.env_eSDK, self.tmpdir_eSDKQA, cmd)

    @testcase(1477)
    def test_Node_js_installation(self):
        added = False

        try:
            cmd = 'devtool add %s ' % self.package_nodejs 
            oeSDKExtSelfTest.run_esdk_cmd(self.env_eSDK, self.tmpdir_eSDKQA, cmd)
            added = True
        finally:
            if added:
                cmd = 'devtool reset %s ' % self.package_nodejs 
                oeSDKExtSelfTest.run_esdk_cmd(self.env_eSDK, self.tmpdir_eSDKQA, cmd)

    @testcase(1478)
    def test_recipes_for_Node_js(self):
        added = False
        try:
            cmd = 'devtool add %s ' % self.package_nodejs
            oeSDKExtSelfTest.run_esdk_cmd(self.env_eSDK, self.tmpdir_eSDKQA, cmd)
            added = True

            cmd = 'devtool build %s ' % self.package_nodejs
            oeSDKExtSelfTest.run_esdk_cmd(self.env_eSDK, self.tmpdir_eSDKQA, cmd)
        finally:
            if added:
                cmd = 'devtool reset %s ' % self.package_nodejs
                oeSDKExtSelfTest.run_esdk_cmd(self.env_eSDK, self.tmpdir_eSDKQA, cmd)

    @testcase(1487)
    def test_sdkupdate_devtool(self):
        image = 'core-image-sato'

        tmpdir_publish_eSDK = tempfile.mkdtemp(prefix='publish_eSDK')

        http_service = HTTPService(tmpdir_publish_eSDK)
        http_service.start()
        http_url = "http://127.0.0.1:%d" % http_service.port

        try:
            oeSDKExtSelfTest.generate_eSDK(image)
            ext_sdk_path_sato = oeSDKExtSelfTest.get_eSDK_toolchain(image)
            cmd = "oe-publish-sdk %s %s" % (ext_sdk_path_sato, tmpdir_publish_eSDK)
            subprocess.check_output(cmd, shell=True)

            cmd = 'devtool sdk-update %s' % http_url
            oeSDKExtSelfTest.run_esdk_cmd(self.env_eSDK, tmpdir_publish_eSDK, cmd)
        finally:
            http_service.stop()
            shutil.rmtree(tmpdir_publish_eSDK)

if __name__ == '__main__':
    unittest.main()
