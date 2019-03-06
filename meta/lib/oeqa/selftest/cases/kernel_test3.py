import os
# import fileinput
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, get_bb_var, runCmd

class KernelDev(OESelftestTestCase):
    def test_linuxyoctocustom_local_source(self):
        """
        Summary:     Able to work with my own local sources for a customized linux-yocto kernel
        Expected:    The variables "PREFERRED_PROVIDER_virtual/kernel" and "SRC_URI" should be set successfully
        Product:     Kernel Development
        Author:      Yeoh Ee Peng <ee.peng.yeoh@intel.com>
        Author:      Yeoh Ee Peng <ee.peng.yeoh@intel.com>
        AutomatedBy: Mazliana Mohamad <mazliana.mohamad@intel.com>
        """
        self.append_config(
'''
PREFERRED_PROVIDER_virtual/kernel = 'linux-yocto-custom'
''')
#        src_uri = 'SRC_URI = "git://git.yoctoproject.org/linux-yocto.git;name=machine;branch=${KBRANCH}; \
#           git://git.yoctoproject.org/yocto-kernel-cache;type=kmeta;name=meta;branch=yocto-4.18;destsuffix=${KMETA}" '
        url = 'SRC_URI = "git://%s/linux-yocto;protocol=file;name=machine;branch=${KBRANCH}; git://%s/yocto-kernel-cache;protocol=file;type=kmeta;name=meta;branch=yocto-%s;destsuffix=${KMETA}" '%(kernel_local_repo_path,kernel_local_repo_path,linux_kernel_version)
        result = runCmd('bitbake virtual/kernel')
        pn = 'linux-yocto-custom'
        src_url = get_bb_var('SRC_URI', pn)
        src_url.replace(src_url, url) 
#        with fileinput.FileInput(recipefile, inplace=True) as file:
#            for line in file:
#                replace = line.replace(src_uri, url)
#                sys.stdout.write(replace)
        os.chdir(self.builddir)
        result = runCmd('bitbake virtual/kernel -c cleansstate')
        result = runCmd('bitbake virtual/kernel')
        result = runCmd('bitbake virtual/kernel -e | grep SRC_URI= ')
        self.assertIn('git://%s'%kernel_local_repo_path ,result.output)