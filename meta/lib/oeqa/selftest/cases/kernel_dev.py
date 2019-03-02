import sys
import os
import re
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, runqemu, get_bb_var, runCmd
from oeqa.utils.git import GitRepo, GitError

class KernelDev(OESelftestTestCase):

    def setUp(self):
        #common prerequisites
        super(KernelDev, self).setUp()
        global build_path, poky_path
        self.recipe = 'core-image-minimal'
        self.machine = 'qemux86-64'
        self.write_config(
'''
MACHINE = '%s'
'''
% (self.machine)
       )
        bitbake(self.recipe)
        result = runCmd('bitbake virtual/kernel -e | grep LINUX_VERSION= | cut -b 16-19')
        linux_kernel_version = result.output
        build_path = os.environ.get('BUILDDIR')
        poky_path, tail = os.path.split(build_path)
        poky_dir = os.chdir(poky_path)
        layername = 'meta-kerneltest'
        result = runCmd('bitbake-layers create-layer %s' %layername)
        self.assertTrue(os.path.exists(layername), '%s should exist' % layername)
        result =runCmd('mkdir -p ' + layername +'/recipes-kernel/linux/linux-yocto/')
        result =runCmd('mkdir -p ' + layername +'/recipes-kernel/linux/linux-yocto-custom/')
        result =runCmd('touch ' + layername + '/recipes-kernel/linux/linux-yocto_4%.bbappend')       
        path_copy_from = poky_path + ('/meta/recipes-kernel/linux/linux-yocto_%s.bb' %linux_kernel_version)
        path_copy_to = poky_path + ('/%s/recipes-kernel/linux/linux-yocto-custom_%s.bb' %(layername, linux_kernel_version))
        result = runCmd('cp %s %s' %(path_copy_from, path_copy_to))
        build_dir = os.chdir(build_path)
        result = runCmd('bitbake-layers add-layer ../%s' %layername)
        result = runCmd('bitbake-layers show-layers')
        find_in_contents = re.search(re.escape(layername) + r'\s+', result.output)
        self.assertTrue(find_in_contents, "%s found in layers\n%s" % (layername, result.output))
    
    def test_apply_patches(self):
        #tc01_kd_apply_patches
        result = runCmd('echo This is a test to apply a patch to the kernel. >> tmp/work-shared/qemux86-64/kernel-source/README')
        #This test step adds modified file 'README' to git and creates a patch file '0001-KERNEL-DEV-TEST-CASE.patch' at the same location as file 
        repo = GitRepo('tmp/work-shared/qemux86-64/kernel-source', is_topdir=True)    
        git_work_tree = os.path.abspath('tmp/work-shared/qemux86-64/kernel-source/README')
        repo.run_cmd('add %s' %(git_work_tree))
        commit_message = 'KERNEL DEV TEST CASE'
        git_commit = ['commit', '-m', commit_message]
        repo.run_cmd(git_commit) 
        git_patch = ['format-patch', '-1']
        repo.run_cmd(git_patch)
        poky_dir = os.chdir(poky_path)
        patch_file = build_path + '/tmp/work-shared/qemux86-64/kernel-source/0001-KERNEL-DEV-TEST-CASE.patch'
        linux_yocto_path = poky_path + '/meta-kerneltest/recipes-kernel/linux/linux-yocto/'
        result = runCmd('mv %s %s' %(patch_file, linux_yocto_path))
        self.assertFalse(os.path.exists(patch_file))
        recipe_append = poky_path + '/meta-kerneltest/recipes-kernel/linux/linux-yocto_4%.bbappend'
        with open (recipe_append, 'w') as file:
            file.write('SRC_URI += \'file://0001-KERNEL-DEV-TEST-CASE.patch\'' + '\n')
            file.write('FILESEXTRAPATHS_prepend := \'${THISDIR}/${PN}:\'')
        readme_path = build_path + '/tmp/work-shared/qemux86-64/kernel-source/README'
        result = runCmd('rm %s ' %readme_path)
        self.assertFalse(os.path.exists(readme_path))  
        result = runCmd('bitbake virtual/kernel -c cleansstate')  
        result = runCmd('bitbake virtual/kernel -c patch')
        self.assertTrue(os.path.exists(readme_path))  
        result = runCmd('tail -n 1 %s ' %readme_path)
        self.assertEqual(result.output, 'This is a test to apply a patch to the kernel.')