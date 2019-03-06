import os
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, runqemu, get_bb_var, runCmd
from oeqa.utils.git import GitRepo, GitError

class KernelDev(OESelftestTestCase):
    @classmethod 
    def setUpClass(cls):
        global poky_path, kernel_local_repo_path, linux_kernel_version, linuxkernelversion
        super(KernelDev, cls).setUpClass()
#        custom_machine = 'qemux86-64'
#        machine_conf = 'MACHINE = "%s"\n' %custom_machine
#        cls.set_machine_config(cls, machine_conf)
        cls.image = 'core-image-minimal'
        bitbake(cls.image)
        builddir = os.environ.get('BUILDDIR')
        poky_path = os.path.dirname(builddir)
        base_path = os.path.dirname(poky_path)
        '''Grep linux kernel version'''
        result = runCmd('bitbake virtual/kernel -e | grep LINUX_VERSION= > kernel_version')
        with open ('kernel_version', 'r') as file:
           for line in file:
               linux_kernel_version = line.strip()
        linux_kernel_version = linux_kernel_version.split("\"")[1]
        linux_kernel_version = linux_kernel_version.split(".")[0] + "." + linux_kernel_version.split(".")[1]
        linuxkernelversion = linux_kernel_version.split(".")[0]
        '''Kernel recipe directory structure'''
        cls.layername = 'meta-kerneltest'
        result = runCmd('bitbake-layers create-layer %s' %cls.layername, cwd=poky_path)
        cls.layerpath = os.path.join(poky_path, cls.layername)
        result =runCmd('mkdir -p %s/recipes-kernel/linux/linux-yocto/' %cls.layername, cwd=poky_path)
        result =runCmd('mkdir -p %s/recipes-kernel/linux/linux-yocto-custom/' %cls.layername, cwd=poky_path)
        result =runCmd('touch %s/recipes-kernel/linux/linux-yocto_%s%%.bbappend' %(cls.layername ,linuxkernelversion), cwd=poky_path)       
        src = poky_path + ('/meta/recipes-kernel/linux/linux-yocto_%s.bb' %linux_kernel_version)
        dest = poky_path + ('/%s/recipes-kernel/linux/linux-yocto-custom_%s.bb' %(cls.layername, linux_kernel_version))
        result = runCmd('cp %s %s' %(src, dest))
        result = runCmd('bitbake-layers add-layer ../%s' %cls.layername, cwd=builddir)
        '''Kernel Local Repo'''
        result = runCmd('mkdir -p kernel_local_repo', cwd=base_path)
        kernel_local_repo_path = os.path.join(base_path, 'kernel_local_repo')
        result = runCmd('git clone git://git.yoctoproject.org/yocto-kernel-cache', cwd=kernel_local_repo_path)
        kernelcache_path = os.path.join(kernel_local_repo_path, 'yocto-kernel-cache')
        result = runCmd('git checkout yocto-%s' %linux_kernel_version, cwd=kernelcache_path)
        result = runCmd('git clone git://git.yoctoproject.org/linux-yocto', cwd=kernel_local_repo_path)
        linuxyocto_path = os.path.join(kernel_local_repo_path, 'linux-yocto')
        result = runCmd('git checkout v%s/standard/base' %linux_kernel_version, cwd =linuxyocto_path)
        
    @classmethod
    def tearDownClass(cls):
        runCmd('bitbake-layers remove-layer %s' %cls.layername, ignore_status=True)
        runCmd('rm -rf %s' %cls.layerpath)
        super(KernelDev, cls).tearDownClass()

    def test_apply_patches(self):
        #TC_KD_01-Applying Patches
        """
        Summary:     Able to apply a single patch to the Linux kernel source
        Expected:    The README file should exist and the patch changes should be displayed at the end of the file. 
        Product:     Kernel Development
        Author:      Yeoh Ee Peng <ee.peng.yeoh@intel.com>
        AutomatedBy: Mazliana Mohamad <mazliana.mohamad@intel.com>
        """
        self.builddir = os.environ.get('BUILDDIR')
        poky_path = os.path.dirname(self.builddir)
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
        patch_file = self.builddir + '/tmp/work-shared/qemux86-64/kernel-source/0001-KERNEL-DEV-TEST-CASE.patch'
        layername = 'meta-kerneltest'
        linux_yocto_path = poky_path + ('/%s/recipes-kernel/linux/linux-yocto/' %layername)
        result = runCmd('mv %s %s' %(patch_file, linux_yocto_path), cwd=self.builddir)
        self.assertFalse(os.path.exists(patch_file))
        recipe_append = poky_path + ('/%s/recipes-kernel/linux/linux-yocto_%s%%.bbappend' %(layername,linuxkernelversion))
        with open (recipe_append, 'w') as file:
            file.write('SRC_URI += \'file://0001-KERNEL-DEV-TEST-CASE.patch\'' + '\n')
            file.write('FILESEXTRAPATHS_prepend := \'${THISDIR}/${PN}:\'')
        readme_file = self.builddir + '/tmp/work-shared/qemux86-64/kernel-source/README'
        result = runCmd('rm %s ' %readme_file)
        self.assertFalse(os.path.exists(readme_file))  
        result = runCmd('bitbake virtual/kernel -c cleansstate')  
        result = runCmd('bitbake virtual/kernel -c patch')
        self.assertTrue(os.path.exists(readme_file))  
        result = runCmd('tail -n 1 %s ' %readme_file)
        self.assertEqual(result.output, 'This is a test to apply a patch to the kernel.')
        
    def test_linuxyocto_local_source(self):
        #TC_KD_02-linux-yocto_Local_Source
        """
        Summary:     Able to work with my own Linux kernel sources
        Expected:    Bitbake variables output should display that the SRC_URI variable
        Product:     Kernel Development
        Author:      Yeoh Ee Peng <ee.peng.yeoh@intel.com>
        AutomatedBy: Mazliana Mohamad <mazliana.mohamad@intel.com>
        """
        self.append_config(
'''
PREFERRED_VERSION_linux-yocto_qemux86-64 = '%s%%'
'''
% (linux_kernel_version)
       )
        url = "SRC_URI = \"git://%s/linux-yocto;protocol=file;name=machine;branch=${KBRANCH}; git://%s/yocto-kernel-cache;protocol=file;type=kmeta;name=meta;branch=yocto-%s;destsuffix=${KMETA}\"" %(kernel_local_repo_path,kernel_local_repo_path,linux_kernel_version)
        layername = 'meta-kerneltest'
        recipe_append = poky_path + ('/%s/recipes-kernel/linux/linux-yocto_%s%%.bbappend' %(layername,linuxkernelversion))
        with open (recipe_append, 'w') as file:
            file.write(url)
        os.chdir(self.builddir)
        result = runCmd('bitbake virtual/kernel -c cleansstate')
        result = runCmd('bitbake virtual/kernel')
        result = runCmd('bitbake virtual/kernel -e | grep "SRC_URI="')
        self.assertIn('git://%s'%kernel_local_repo_path ,result.output)