import sys
import os
import logging
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, runqemu, get_bb_var, runCmd
from oeqa.utils.git import GitRepo, GitError

class KernelDev(OESelftestTestCase):

  def setUpLocal(self):
       sys.stdout = sys.__stdout__
       print ('\n inside setUpLocal \n')
       super(KernelDev, self).setUpLocal()
       self.recipe = 'core-image-minimal'
       self.machine = 'qemux86-64'
       self.write_config(
"""
MACHINE = "%s"
"""
% (self.machine)
       )
       print (get_bb_var('MACHINE'))
        
  
  def test_runCommand(self):
       # This test step updates the README file
       sys.stdout = sys.__stdout__ 
       print ("\n\ninside test_runCommand\n\n")
       #writetoreadme = runCmd("echo This is a test to apply a patch to the kernel. >> tmp/work-shared/qemux86-64/kernel-source/README")
      # self.assertEqual(writetoreadme.output, "")
       
       
  def test_gitadd(self):
       # This test step updates the README file
       sys.stdout = sys.__stdout__ 
       print ("\n\ninside test_gidadd\n\n")
       writetoreadme = runCmd("echo This is a test to apply a patch to the kernel. >> tmp/work-shared/qemux86-64/kernel-source/README")
       self.assertEqual(writetoreadme.output, "")
      
       
       #This test step adds modified file "README" to git and creates a patch file "0001-KERNEL-DEV-TEST-CASE.patch" at the same location as file 
       repo = GitRepo("tmp/work-shared/qemux86-64/kernel-source", is_topdir=True) 
       os_path = os.path
              
       GIT_WORK_TREE = os.path.abspath('tmp/work-shared/qemux86-64/kernel-source/README')
       
       repo.run_cmd('add %s' %(GIT_WORK_TREE))
       
       commit_message = "KERNEL DEV TEST CASE"
       git_cmd_commit = ['commit', '-m', commit_message]
       repo.run_cmd(git_cmd_commit) 

       git_cmd_patch = ['format-patch', '-1']
       repo.run_cmd(git_cmd_patch)

  def test_move(self):
        
       sys.stdout = sys.__stdout__ 
       build_path = os.environ.get('BUILDDIR')
       print ("\n\ninside test_move\n\n")
       #logging.debug('build_path = %s' %build_path)
       print ('build_path = %s' %build_path)
       poky_path, tail = os.path.split(build_path)
       print ('poky_path = %s' %poky_path)
       print ('tail = %s' %tail)
       poky_dir = os.chdir(poky_path)
       print ('poky_dir = %s' %poky_dir)
       #file_path = build + tmp/work-shared/qemux86-64/kernel-source/0001-KERNEL-DEV-TEST-CASE.patch
       patch_file = build_path + '/tmp/work-shared/qemux86-64/kernel-source/0001-KERNEL-DEV-TEST-CASE.patch'
       new_path = poky_path + '/meta-kernelautomated/recipes-kernel/linux/linux-yocto/'
       print ('new_path = %s' %new_path)
              
       result = runCmd('mv %s %s' %(patch_file, new_path))
       self.assertEqual(result.output, "")
       file_name = poky_path + '/meta-kernelautomated/recipes-kernel/linux/linux-yocto_4%.bbappend'
       print ('file_name = %s' %file_name)
       
       with open (file_name, 'w') as file:
         file.write("SRC_URI += \"file://0001-KERNEL-DEV-TEST-CASE.patch\"" + "\n")
         file.write('FILESEXTRAPATHS_prepend := \"${THISDIR}/${PN}:\"')
       file.close() 

       readme_path = build_path + '/tmp/work-shared/qemux86-64/kernel-source/README'
       print ('readme_path = %s' %readme_path)  
       remove_readme_file = runCmd('rm %s ' %readme_path)
       print ('readme removed')
       self.assertEqual(remove_readme_file.output, "")  
       run_cleanstate = runCmd('bitbake virtual/kernel -c cleansstate')  
       print ('cleanstate')
       run_buildpatch = runCmd('bitbake virtual/kernel -c patch')  
       print ('build patch')
       file_exists = os.path.exists(readme_path)
       print ('file_exists = %s' %file_exists)
       tail_readme_file = runCmd('tail %s ' %readme_path)
       print (tail_readme_file.output)
        