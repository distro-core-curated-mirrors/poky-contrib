import os
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, runCmd
from oeqa.utils.git import GitRepo, GitError

class KernelDev(OESelftestTestCase):
    @classmethod 
    def setUpClass(cls):
        super(KernelDev, cls).setUpClass()
        custom_machine = 'qemux86-64'
        cls.machine_conf = 'MACHINE = "%s"\n' %custom_machine
        cls.set_machine_config(cls, cls.machine_conf)
        cls.image = 'core-image-minimal'
        bitbake(cls.image)
        builddir = os.environ['BUILDDIR']
        cls.poky_path = os.path.dirname(builddir)
        base_path = os.path.dirname(cls.poky_path)
        #Get and take note of the linux-yocto kernel version (the first and two numbers , for example: 5 and 5.0)
        result = runCmd('bitbake virtual/kernel -e | grep LINUX_VERSION= > kernel_version')
        with open ('kernel_version', 'r') as file:
            for line in file:
                linux_yocto_kernel_version = line.strip()
        linux_yocto_kernel_version = linux_yocto_kernel_version.split("\"")[1]
        cls.linux_yocto_kernel_version = linux_yocto_kernel_version.split(".")[0] + "." + linux_yocto_kernel_version.split(".")[1]
        cls.linuxyoctokernelversion = cls.linux_yocto_kernel_version.split(".")[0]
        #Create the recipe directory structure inside the created layer
        cls.layername = 'meta-kerneltest'
        result = runCmd('bitbake-layers create-layer %s' %cls.layername, cwd=cls.poky_path)
        cls.layerpath = os.path.join(cls.poky_path, cls.layername)
        result =runCmd('mkdir -p %s/recipes-kernel/linux/linux-yocto/' %cls.layername, cwd=cls.poky_path)
        result =runCmd('mkdir -p %s/recipes-kernel/linux/linux-yocto-custom/' %cls.layername, cwd=cls.poky_path)
        result =runCmd('touch %s/recipes-kernel/linux/linux-yocto_%s%%.bbappend' %(cls.layername ,cls.linuxyoctokernelversion), cwd=cls.poky_path)       
        src = os.path.join(cls.poky_path, 'meta/recipes-kernel/linux/linux-yocto_%s.bb' %cls.linux_yocto_kernel_version)
        dest = os.path.join(cls.poky_path, '%s/recipes-kernel/linux/linux-yocto-custom_%s.bb' %(cls.layername, cls.linux_yocto_kernel_version))
        result = runCmd('cp %s %s' %(src, dest))
        result = runCmd('bitbake-layers add-layer ../%s' %cls.layername, cwd=builddir)

    @classmethod
    def tearDownClass(cls):
        runCmd('bitbake-layers remove-layer %s' %cls.layername, ignore_status=True)
        runCmd('rm -rf %s' %cls.layerpath)
        super(KernelDev, cls).tearDownClass()
    
    def setUp(self):
        super(KernelDev, self).setUp()
        self.set_machine_config(self.machine_conf)

    def test_apply_patches(self):
        """
        Summary:     Able to apply a single patch to the Linux kernel source
        Expected:    The README file should exist and the patch changes should be displayed at the end of the file. 
        Product:     Kernel Development
        Author:      Yeoh Ee Peng <ee.peng.yeoh@intel.com>
        AutomatedBy: Mazliana Mohamad <mazliana.mohamad@intel.com>
        """
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
        patch_file = os.path.join(self.builddir, 'tmp/work-shared/qemux86-64/kernel-source/0001-KERNEL-DEV-TEST-CASE.patch')
        linux_yocto_path = os.path.join(self.poky_path,'%s/recipes-kernel/linux/linux-yocto/' %self.layername)
        result = runCmd('mv %s %s' %(patch_file, linux_yocto_path), cwd=self.builddir)
        self.assertFalse(os.path.exists(patch_file))
        recipe_append = os.path.join(self.poky_path,'%s/recipes-kernel/linux/linux-yocto_%s%%.bbappend' %(self.layername,self.linuxyoctokernelversion))
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