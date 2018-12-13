import sys
import os
import logging
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, runqemu, get_bb_var, runCmd
from oeqa.utils.git import GitRepo, GitError

class KernelDevTc(OESelftestTestCase):
    def test_createpatch(self):
        writetoreadme = runCmd("echo This is a test to apply a patch to the kernel. >> tmp/work-shared/qemux86-64/kernel-source/README")
        self.assertEqual(writetoreadme.output, "")
        #This test step adds modified file "README" to git and creates a patch file "0001-KERNEL-DEV-TEST-CASE.patch" at the same location as file 
        repo = GitRepo("tmp/work-shared/qemux86-64/kernel-source", is_topdir=True)    
        git_work_tree = os.path.abspath('tmp/work-shared/qemux86-64/kernel-source/README')
        repo.run_cmd('add %s' %(git_work_tree))
        commit_message = "KERNEL DEV TEST CASE"
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
        self.assertEqual(result.output, "")
        file_name = poky_path + '/meta-kernelautomated/recipes-kernel/linux/linux-yocto_4%.bbappend'
        with open (file_name, 'w') as file:
            file.write("SRC_URI += \"file://0001-KERNEL-DEV-TEST-CASE.patch\"" + "\n")
            file.write('FILESEXTRAPATHS_prepend := \"${THISDIR}/${PN}:\"')
        readme_path = build_path + '/tmp/work-shared/qemux86-64/kernel-source/README'
        remove_readme_file = runCmd('rm %s ' %readme_path)
        self.assertEqual(remove_readme_file.output, "")  
        run_cleanstate = runCmd('bitbake virtual/kernel -c cleansstate')  
        run_buildpatch = runCmd('bitbake virtual/kernel -c patch')  
        file_exists = os.path.exists(readme_path)
        tail_readme_file = runCmd('tail %s ' %readme_path)
        