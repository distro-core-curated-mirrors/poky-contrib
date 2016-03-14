__author__ = 'cosscat'

import os
import base
from base import basic_functionality as bfunc

"""
Important note:
Because the cloning and all other stuff.
"""


class GitEssentials:

    base_dir = ''

    def __init__(self, base_dir):

        self.base_dir = base_dir
        # Test if base_dir exists, if not create it and chdir into it
        # Also: should I check for correct file permissions or free disk space?
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        os.chdir(base_dir)

    @staticmethod
    def is_cloned(dirname):
        """
        Look for a .git directory inside dirname
        :param dirname: Directory to look inside for .git directory
        :return: True/False if .git directory found or not
        """

        return os.path.isdir(os.path.join(dirname, '.git'))

    def clone(self, repo, base_dir, clone_name="poky"):
        """
        Clone the specified repo inside the base_dir with name as clone_name
        :param repo: git url repo
        :param base_dir: top dir to clone into
        :param clone_name: dir name of clone
        :return:
        """
        clone_dir = os.path.join(base_dir, clone_name)
        if self.is_cloned(clone_dir):
            # No need to re clone it, just sync master
            self.sync_local_branch(clone_dir, 'origin', 'master')
            return 0
        os.chdir(base_dir)
        clone_command = "git clone {} {}".format(repo, clone_name)
        retcode, retval = bfunc.run_command_locally(clone_command)
        return retcode

    @staticmethod
    def checkout(clone_dir, commit='master'):
        os.chdir(clone_dir)
        chk_command = "git checkout {}".format(commit)
        retcode, retval = bfunc.run_command_locally(chk_command)
        return retcode

    @staticmethod
    def fetch(clone_dir, repo, remote_branch):
        os.chdir(clone_dir)
        fetch_command = "git fetch {} {}".format(repo, remote_branch)
        retcode, retval = bfunc.run_command_locally(fetch_command)
        return retcode

    @staticmethod
    def add_remote(clone_dir, remote_name, remote_repo):
        os.chdir(clone_dir)
        add_rmt_command = "git remote add {} {}".format(remote_name, remote_repo)
        retcode, retval = bfunc.run_command_locally(add_rmt_command)
        if retcode:
            if 'remote contrib already exists' not in retval:
                raise ValueError(retval)
            retcode = 0
        return retcode

    @staticmethod
    def reset_hard(clone_dir, repo, branch):
        """
        Hard reset the local branch
        :param clone_dir: local clone dir
        :param repo: remote repo (eg. origin, contrib)
        :param branch: branch to reset (eg. master, ross/mut)
        :return: Exit code of the command
        """
        os.chdir(clone_dir)
        reset_hard_cmd = 'git reset --hard %s/%s' % (repo, branch)
        retcode, retval = bfunc.run_command_locally(reset_hard_cmd)
        return retcode

    def sync_local_branch(self, clone_dir, repo, branch):
        """
        Sync local branch with remote branch
        Eg: sync_local_branch('/home/user/poky', 'origin', 'master')
            sync_local_branch('/home/user/poky', 'contrib', 'ross/mut')
        :param clone_dir: local clone dir
        :param repo: remote repo (eg. origin, contrib)
        :param branch: branch to sync (eg. master, ross/mut)
        :return:
        """
        try:
            self.fetch(clone_dir, repo, branch)
            self.checkout(clone_dir, branch)
            self.reset_hard(clone_dir, repo, branch)
        except:
            raise Exception('Failed to sync local branch.')

class Testing_Harness(base.basic_functionality): # nice name huh? :)
    def __init__(self):
        pass

    def bitbake(self, *args):
        bb_command = "cd {} && source oe-init-build-env {} && bitbake ".format(self.poky_dir, self.build_dir)
        for elem in args:
            bb_command += elem + ' '
        print bb_command
        #self.run_comamd_locally(bb_command)


# HOW TO USE GitEssentials

# base_dir = '/home/daniel/tmptestdir'
# from testing_env import GitEssentials
# g = GitEssentials(base_dir)
#
# # Clone/re sync poky
# g.clone('git://git.yoctoproject.org/poky', base_dir, 'poky')
# # Add contrib repo
# poky_dir = os.path.join(base_dir, 'poky')
# g.add_remote(poky_dir, 'contrib', 'git://git.yoctoproject.org/poky-contrib')
#
# # Clone/ re sync meta-qt3, meta-qt4, meta-intel
# layers_repo_dict = {'meta-intel': 'git://git.yoctoproject.org/meta-intel',
#                     'meta-qt3': 'git://git.yoctoproject.org/meta-qt3',
#                     'meta-qt4': 'git://git.yoctoproject.org/meta-qt4'}
#
# for layer in layers_repo_dict:
#     g.clone(layers_repo_dict[layer], poky_dir, layer)
#
# # Checkout a specific commit
# g.checkout(poky_dir)  # checkout master first
# # or
# # g.sync_local_branch(poky_dir, 'origin', 'master')
# commit = '8debfea81e69d038bd2d56314b272cb74f5582ed'
# g.checkout(poky_dir, commit)
#
# # Checkout ross/mut (Optionally)
# g.sync_local_branch(poky_dir, 'contrib', 'ross/mut')
