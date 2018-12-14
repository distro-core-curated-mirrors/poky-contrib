import sys
import os
import re
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, runqemu, get_bb_var, runCmd
from oeqa.utils.git import GitRepo, GitError

class KernelDev(OESelftestTestCase):

    def setUpLocal(self):
        super(KernelDev, self).setUpLocal()
        self.recipe = 'core-image-minimal'
        self.machine = 'qemux86-64'
        self.write_config(
'''
MACHINE = '%s'
'''
% (self.machine)
       )
        bitbake(self.recipe)

    def test_getMachine(self):
        getmachine = get_bb_var('MACHINE')
        self.assertEqual(getmachine, 'qemux86-64')

    def test_create_layer_recipe(self):
        result = runCmd('bitbake virtual/kernel -e | grep LINUX_VERSION=')
        getlinuxversion = runCmd('bitbake virtual/kernel -e | grep LINUX_VERSION= > kernel_version')
        with open ('kernel_version', 'r') as file:
           for line in file:
               linux_kernel_version = line.strip()
        self.assertEqual(result.output, linux_kernel_version)
        linux_kernel_version = linux_kernel_version.split('\"')[1]
        linux_kernel_version = linux_kernel_version.split('.')[0] + '.' + linux_kernel_version.split('.')[1]
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
        path_copy_from = poky_path + ('/meta/recipes-kernel/linux/linux-yocto_%s.bb' %linux_kernel_version)
        path_copy_to = poky_path + ('/%s/recipes-kernel/linux/linux-yocto_custom_%s.bb' %(layername, linux_kernel_version))
        result_copy = runCmd('cp %s %s' %(path_copy_from, path_copy_to))
        #with open (path_copy_to, 'a') as file:
         #file.write('PV = \'${%s}\''  %linux_kernel_version )
        build_dir = os.chdir(build_path)
        result = runCmd('bitbake-layers add-layer ../%s' %layername)
    
    def test_createpatch(self):
        writetoreadme = runCmd('echo This is a test to apply a patch to the kernel. >> tmp/work-shared/qemux86-64/kernel-source/README')
        self.assertEqual(writetoreadme.output, '')
        #This test step adds modified file 'README' to git and creates a patch file '0001-KERNEL-DEV-TEST-CASE.patch' at the same location as file 
        repo = GitRepo('tmp/work-shared/qemux86-64/kernel-source', is_topdir=True)    
        git_work_tree = os.path.abspath('tmp/work-shared/qemux86-64/kernel-source/README')
        repo.run_cmd('add %s' %(git_work_tree))
        commit_message = 'KERNEL DEV TEST CASE'
        git_cmd_commit = ['commit', '-m', commit_message]
        repo.run_cmd(git_cmd_commit) 
        git_cmd_patch = ['format-patch', '-1']
        repo.run_cmd(git_cmd_patch)

    def test_existingpatch(self):
        build_path = os.environ.get('BUILDDIR')
        poky_path, tail = os.path.split(build_path)
        poky_dir = os.chdir(poky_path)
        patch_file = build_path + '/tmp/work-shared/qemux86-64/kernel-source/0001-KERNEL-DEV-TEST-CASE.patch'
        new_path = poky_path + '/meta-kernelautomated/recipes-kernel/linux/linux-yocto/'
        result = runCmd('mv %s %s' %(patch_file, new_path))
        self.assertEqual(result.output, '')
        file_name = poky_path + '/meta-kernelautomated/recipes-kernel/linux/linux-yocto_4%.bbappend'
        with open (file_name, 'w') as file:
            file.write('SRC_URI += \'file://0001-KERNEL-DEV-TEST-CASE.patch\'' + '\n')
            file.write('FILESEXTRAPATHS_prepend := \'${THISDIR}/${PN}:\'')
        readme_path = build_path + '/tmp/work-shared/qemux86-64/kernel-source/README'
        remove_readme_file = runCmd('rm %s ' %readme_path)
        self.assertEqual(remove_readme_file.output, '')  
        run_cleanstate = runCmd('bitbake virtual/kernel -c cleansstate')  
        run_buildpatch = runCmd('bitbake virtual/kernel -c patch')  
        file_exists = os.path.exists(readme_path)
        tail_readme_file = runCmd('tail %s ' %readme_path)
        self.assertEqual(tail_readme_file.output, 'This is a test to apply a patch to the kernel')
        
        
        
