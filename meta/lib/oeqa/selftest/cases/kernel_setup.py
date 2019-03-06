import os
import re
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, runqemu, get_bb_var, runCmd

class KernelDev(OESelftestTestCase):
    def setUp(self):
        '''
        Each test case depend on prerequisites
        Problem: This prerequisites should be able setup on time only so that we not repetative same process. Also reduce time to rebuild image
        '''
        global linux_kernel_version, poky_path, linux_yocto_path, recipe, recipe_append, kernel_local_repo_path
        super(KernelDev, self).setUp()
        self.image = 'core-image-minimal'
        self.machine = 'qemux86-64'
        self.set_machine_config(
'''
MACHINE = '%s'
'''
% (self.machine)
       )
        bitbake(self.image)
        result = runCmd('bitbake virtual/kernel -e | grep LINUX_VERSION= | cut -b 16-19')
        linux_kernel_version = result.output
        poky_path = os.path.dirname(os.path.realpath(self.builddir))
        layername = 'meta-kerneltest'
        result = runCmd('bitbake-layers create-layer %s' %layername, cwd=poky_path)
        layerpath = os.path.join(poky_path, layername)
        self.assertTrue(os.path.exists(layerpath), '%s should exist' % layerpath)
        result =runCmd('mkdir -p %s/recipes-kernel/linux/linux-yocto/' %layername, cwd=poky_path)
        linux_yocto_path = os.path.join(poky_path, 'meta-kerneltest/recipes-kernel/linux/linux-yocto/')
        result =runCmd('mkdir -p %s/recipes-kernel/linux/linux-yocto-custom/' %layername, cwd=poky_path)
        result =runCmd('touch %s/recipes-kernel/linux/linux-yocto_4%%.bbappend' %layername, cwd=poky_path) 
        recipe_append = os.path.join(poky_path, 'meta-kerneltest/recipes-kernel/linux/linux-yocto_4%.bbappend')      
        src_recipe = os.path.join(poky_path,'meta/recipes-kernel/linux/linux-yocto_%s.bb' %linux_kernel_version)
        recipe = os.path.join(poky_path, '%s/recipes-kernel/linux/linux-yocto-custom_%s.bb' %(layername, linux_kernel_version))
        result = runCmd('cp %s %s' %(src_recipe, recipe))
        result = runCmd('bitbake-layers add-layer ../%s' %layername, cwd=self.builddir)
        result = runCmd('bitbake-layers show-layers', cwd=self.builddir)
        find_in_contents = re.search(re.escape(layername) + r'\s+', result.output)
        self.assertTrue(find_in_contents, "%s found in layers\n%s" % (layername, result.output))
        
        base_path = os.path.dirname(poky_path)
        result = runCmd('mkdir kernel_local_repo', cwd=base_path)
        kernel_local_repo_path = os.path.join(base_path, 'kernel_local_repo')
        result = runCmd('git clone git://git.yoctoproject.org/yocto-kernel-cache', cwd=kernel_local_repo_path)
        kernelcache_path = os.path.join(kernel_local_repo_path, 'yocto-kernel-cache')
        result = runCmd('git checkout yocto-4.18', cwd=kernelcache_path)
        result = runCmd('git clone git://git.yoctoproject.org/linux-yocto', cwd=kernel_local_repo_path)
        linuxyocto_path = os.path.join(kernel_local_repo_path, 'linux-yocto')
        result = runCmd('git checkout v%s/standard/base' %linux_kernel_version, cwd =linuxyocto_path)

    def tearDown(self):
        runCmd('bitbake-layers remove-layer %s' % layername)
        runCmd('rm -rf %s' % layerpath)
        runCmd('rm -rf %s' % kernel_local_repo_path)
        super(KernelDev, self).tearDown()

    
#    def test_agetMachine(self):
#        getmachine = get_bb_var('MACHINE')
#        self.assertEqual(getmachine, 'qemux86-64')