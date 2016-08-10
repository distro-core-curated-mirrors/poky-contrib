import shutil
import subprocess
import urllib.request
from oeqa.oetest import oeSDKExtTest
from oeqa.utils.decorators import *

class DevtoolTest(oeSDKExtTest):
    @classmethod
    def setUpClass(self):
        self.myapp_src = os.path.join(self.tc.sdkextfilesdir, "myapp")
        self.myapp_dst = os.path.join(self.tc.sdktestdir, "myapp")
        shutil.copytree(self.myapp_src, self.myapp_dst)

        self.myapp_cmake_src = os.path.join(self.tc.sdkextfilesdir, "myapp_cmake")
        self.myapp_cmake_dst = os.path.join(self.tc.sdktestdir, "myapp_cmake")
        shutil.copytree(self.myapp_cmake_src, self.myapp_cmake_dst)

    def _test_devtool_build(self, directory):
        self._run('devtool add myapp %s' % directory)
        try:
            self._run('devtool build myapp')
        except Exception as e:
            print(e.output)
            self._run('devtool reset myapp')
            raise e
        self._run('devtool reset myapp')

    def _test_devtool_build_package(self, directory):
        self._run('devtool add myapp %s' % directory)
        try:
            self._run('devtool package myapp')
        except Exception as e:
            print(e.output)
            self._run('devtool reset myapp')
            raise e
        self._run('devtool reset myapp')

    def test_devtool_location(self):
        output = self._run('which devtool')
        self.assertEqual(output.startswith(self.tc.sdktestdir), True, \
            msg="Seems that devtool isn't the eSDK one: %s" % output)
    
    @skipUnlessPassed('test_devtool_location')
    def test_devtool_add_reset(self):
        self._run('devtool add myapp %s' % self.myapp_dst)
        self._run('devtool reset myapp')
    
    @testcase(1473)
    @skipUnlessPassed('test_devtool_location')
    def test_devtool_build_make(self):
        self._test_devtool_build(self.myapp_dst)
    
    @testcase(1474)
    @skipUnlessPassed('test_devtool_location')
    def test_devtool_build_esdk_package(self):
        self._test_devtool_build_package(self.myapp_dst)

    @testcase(1479)
    @skipUnlessPassed('test_devtool_location')
    def test_devtool_build_cmake(self):
        self._test_devtool_build(self.myapp_cmake_dst)
    
    @testcase(1482)
    @skipUnlessPassed('test_devtool_location')
    def test_extend_autotools_recipe_creation(self):
        req = 'https://raw.githubusercontent.com/DynamicDevices/meta-example/master/recipes-example/bbexample/bbexample_1.0.bb'
        recipe = "bbexample"
        self._run('devtool add %s %s' % (recipe, req) )
        try:
            self._run('devtool build %s' % recipe)
        except Exception as e:
            print(e.output)
            self._run('devtool reset %s' % recipe)
            raise e
        self._run('devtool reset %s' % recipe)

    @testcase(1484)
    @skipUnlessPassed('test_devtool_location')
    def test_devtool_add_support(self):
        docfile = 'git://github.com/Mange/rtl8192eu-linux-driver.git'
        recipe = 'rtl-linux-driver'
        self._run('devtool add %s %s' % (recipe, docfile) )
        try:
            self._run('devtool build %s' % recipe)
        except Exception as e:
            print(e.output)
            self._run('devtool reset %s' % recipe)
            raise e
        self._run('devtool reset %s' % recipe)

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.myapp_dst)
        shutil.rmtree(self.myapp_cmake_dst)
