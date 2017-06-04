from oeqa.selftest.base import oeSelfTest
from oeqa.utils.commands import runCmd, bitbake, get_bb_var
import os

class Useradd(oeSelfTest):

    def assertnouser(self, user, etcdir):
        with open(etcdir + "/passwd") as f:
            for l in f.readlines():
                self.assertFalse(l.startswith(user + ":"))

    def assertnogroup(self, group, etcdir):
        with open(etcdir + "/group") as f:
            for l in f.readlines():
                self.assertFalse(l.startswith(group + ":"))

    def finduser(self, user, etcdir):
        with open(etcdir + "/passwd") as f:
            for l in f.readlines():
                if l.startswith(user + ":"):
                    return l
        return False

    def findgroup(self, group, etcdir):
        with open(etcdir + "/group") as f:
            for l in f.readlines():
                if l.startswith(group + ":"):
                    return l
        return False

    def test_useradd(self):

        bitbake("useraddtest-a:do_clean")
        bitbake("useraddtest-a:do_patch")

        etcdir = get_bb_var('STAGING_DIR_TARGET', "useraddtest-a") + "/etc"

        self.assertFalse(os.path.exists(etcdir + "/passwd"))

        bitbake("useraddtest-a:do_prepare_sysroot")
        self.add_command_to_tearDown('bitbake -c clean useraddtest-a')

        user = self.finduser("testusera", etcdir)
        self.assertTrue(user, msg="Unable to find user testusera in %s/passwd" % etcdir)
        group = self.findgroup("testgroupa", etcdir)
        self.assertTrue(user, msg="Unable to find user testgroupa in %s/group" % etcdir)

        #bitbake("useraddtest-a -c clean")
        #self.assertnouser("testusera", etcdir)
        #self.assertnogroup("testgroupa", etcdir)


