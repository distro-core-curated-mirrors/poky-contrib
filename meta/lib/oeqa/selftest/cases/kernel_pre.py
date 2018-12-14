import sys
import os
import re
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, runqemu, get_bb_var, runCmd

class KernelDev(OESelftestTestCase):

    def setUpLocal(self):
        super(KernelDev, self).setUpLocal()
        self.recipe = 'core-image-minimal'
        self.machine = 'qemux86-64'
        self.write_config(
"""
MACHINE = "%s"
"""
% (self.machine)
       )
        bitbake(self.recipe)

    def test_agetMachine(self):
        getmachine = get_bb_var('MACHINE')
        self.assertEqual(getmachine, 'qemux86-64')

    def test_bgetLinuxVersion(self):
        result = runCmd('bitbake virtual/kernel -e | grep LINUX_VERSION=')
        getlinuxversion = runCmd('bitbake virtual/kernel -e | grep LINUX_VERSION= > kernel_version')
        with open ('kernel_version', 'r') as file:
           for line in file:
               linux_kernel_version = line.strip()
        self.assertEqual(result.output, linux_kernel_version)
        linux_kernel_version = linux_kernel_version.split("\"")[1]
        linux_kernel_version = linux_kernel_version.split(".")[0] + "." + linux_kernel_version.split(".")[1]
        build_path = os.environ.get('BUILDDIR')
        poky_path, tail = os.path.split(build_path)
        poky_dir = os.chdir(poky_path)
        layername = 'meta-kernelautomated'
        layerpath = os.path.exists(layername)        
        self.assertTrue(os.path.exists(layerpath), '%s should not exist at this point in time' % layerpath)
        result = runCmd('bitbake-layers create-layer %s' %layername)
        self.assertTrue(os.path.exists(layerpath), '%s should exist' % layerpath)
        dir_recipe = runCmd('mkdir -p ' + layername +'/recipes-kernel/linux/')
        dir_linux_yocto =runCmd('mkdir ' + layername +'/recipes-kernel/linux/linux-yocto/')
        dir_linux_yocto_custom =runCmd('mkdir ' + layername +'/recipes-kernel/linux/linux-yocto-custom/')
        recipe_append =runCmd('touch ' + layername + '/recipes-kernel/linux/linux-yocto_4%.bbappend')       
        path_copy_from = poky_path + ("/meta/recipes-kernel/linux/linux-yocto_%s.bb" %linux_kernel_version)
        path_copy_to = poky_path + ("/%s/recipes-kernel/linux/linux-yocto_custom_%s.bb" %(layername, linux_kernel_version))
        result_copy = runCmd('cp %s %s' %(path_copy_from, path_copy_to))
        #with open (path_copy_to, 'a') as file:
         #file.write('PV = \"${%s}\"'  %linux_kernel_version )
        #build_dir = os.chdir(build_path)
        #result = runCmd('bitbake-layers add-layer ../%s' %layername)
        
        
