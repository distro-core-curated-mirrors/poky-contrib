__author__ = 'cosscat'

import os
import base

"""
Important note:
Because the cloning and all other stuff.
"""

class Git_Essentials(base.basic_functionality):
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def clone(self, repo, base_dir, clone_name="poky"):
        dir_to_clone_in = base_dir
        os.chdir(dir_to_clone_in)
        clone_command = "git clone {} {}".format(repo, clone_name)
        self.clone_dir = os.path.join(dir_to_clone_in, clone_name)
        retcode, retval = self.run_command_locally(clone_command)
        return retcode

    def checkout(self, commit):
        os.chdir(self.clone_dir)
        chk_command = "git checkout {}".format(commit)
        retcode, retval = self.run_command_locally(chk_command)
        return retcode

    def fetch(self, repo, remote_branch):
        fetch_command = "git fetch {} {}:{}".format(repo, remote_branch, remote_branch) # blah blah
        retcode, retval = self.run_command_locally(fetch_command)
        return retcode

    def add_remote(self, remote_name, remote_repo):
        add_rmt_command = "git remote add {} {}".format(remote_name, remote_repo)
        retcode, retval = self.run_command_locally(add_rmt_command)
        return retcode


class Testing_Harness(base.basic_functionality): # nice name huh? :)
    def __init__(self):
        pass

    def bitbake(self, *args):
        bb_command = "cd {} && source oe-init-build-env {} && bitbake ".format(self.poky_dir, self.build_dir)
        for elem in args:
            bb_command += elem + ' '
        print bb_command
        #self.run_comamd_locally(bb_command)


