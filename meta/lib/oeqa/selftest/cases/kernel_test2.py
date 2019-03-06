import sys
import os
import re
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, runCmd

class KernelDev(OESelftestTestCase):
    def test_linuxyocto_local_source(self):
        #TC_KD_02-linux-yocto_Local_Source
        """
        Summary:     Able to work with my own Linux kernel sources
        Expected:    Bitbake variables output should display that the SRC_URI variable
        Product:     Kernel Development
        Author:      Yeoh Ee Peng <ee.peng.yeoh@intel.com>
        Author:      Yeoh Ee Peng <ee.peng.yeoh@intel.com>
        AutomatedBy: Mazliana Mohamad <mazliana.mohamad@intel.com>
        """
        self.append_config(
'''
PREFERRED_VERSION_linux-yocto_qemux86-64 = '%s%%'
'''
% (linux_kernel_version)
       )
        url = 'SRC_URI = "git://%s/linux-yocto;protocol=file;name=machine;branch=${KBRANCH}; git://%s/yocto-kernel-cache;protocol=file;type=kmeta;name=meta;branch=yocto-%s;destsuffix=${KMETA}" '%(kernel_local_repo_path,kernel_local_repo_path,linux_kernel_version)
        with open (recipe_append, 'w') as file:
            file.write(url)
        os.chdir(self.builddir)
        result = runCmd('bitbake virtual/kernel -c cleansstate')
        result = runCmd('bitbake virtual/kernel')
        result = runCmd('bitbake virtual/kernel -e | grep "SRC_URI="')
        self.assertIn('git://%s'%kernel_local_repo_path ,result.output)