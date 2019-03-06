import os
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, runCmd
from oeqa.utils.git import GitRepo, GitError

class KernelDevTc(OESelftestTestCase):
    def test_apply_patches(self):
        """
        Summary:     Able to apply a single patch to the Linux kernel source
        Expected:    The README file should exist and the patch changes should be displayed at the end of the file. 
        Product:     Kernel Development
        Author:      Yeoh Ee Peng <ee.peng.yeoh@intel.com>
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
        result = runCmd('mv %s %s' %(patch_file, linux_yocto_path), cwd=self.builddir)
        self.assertFalse(os.path.exists(patch_file))
        with open (recipe_append, 'w') as file:
            file.write('SRC_URI += \'file://0001-KERNEL-DEV-TEST-CASE.patch\'' + '\n')
            file.write('FILESEXTRAPATHS_prepend := \'${THISDIR}/${PN}:\'')
        readme_path = os.path.join(self.builddir, 'tmp/work-shared/qemux86-64/kernel-source/README')
        result = runCmd('rm %s ' %readme_path)
        self.assertFalse(os.path.exists(readme_path))  
        result = runCmd('bitbake virtual/kernel -c cleansstate')  
        result = runCmd('bitbake virtual/kernel -c patch')
        self.assertTrue(os.path.exists(readme_path))  
        result = runCmd('tail -n 1 %s ' %readme_path)
        self.assertEqual(result.output, 'This is a test to apply a patch to the kernel.')