import inspect
import os
import utils

class RepoException(Exception):
    def __init__(self, series, revision, repo, verb=None, custom_msg=None):
        self.series = series
        self.revision = revision
        self.repo = repo
        self.verb = verb
        self.custom_msg = custom_msg

    def __str__(self):
        msg = "Repository exception for series/revision: %s/%s" % (self.series, self.revision)
        if self.custom_msg:
            msg = self.custom_msg
        elif self.verb:
            msg = "Failed to %s the repository %s for series/revision: %s/%s" % (self.verb, self.repo,
                                                                                 self.series, self.revision)
        return msg

class RepoPatchException(RepoException):
    pass

class Repo(object):
    def __init__(self,
                 series, revision,
                 pw_url, pw_project,
                 pw_user, pw_pass,
                 repo_dir, temp_base_dir,
                 remote, stable_branch):
        self.series = series
        self.revision = revision
        self.pw_url = pw_url
        self.pw_user = pw_user
        self.pw_pass = pw_pass
        self.pw_project = pw_project
        self.repo_dir = repo_dir
        self.temp_base_dir = temp_base_dir
        self.remote = remote
        self.stable_branch = stable_branch

        self.temp_dir = utils.get_temp_dir(self.temp_base_dir, self.series, self.revision)
        self.branch_name = utils.branch_name(self.series, self.revision)

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def _exec(self, cmds):
        stack = inspect.stack()
        task_name = stack[1][3]
        return utils.exec_cmds(cmds, self.repo_dir, self.temp_dir, task_name)

    def _add_gitignore(self, pattern):
        """ Add pattern into the repo's .gitignore """
        gitignore = "%s/.gitignore" % self.repo_dir
        pattern_present = False

        try:
            fd = open(gitignore)
            ignorelines = fd.readlines()
            if pattern in ignorelines:
                pattern_present = True
        except IOError:
            pass

        if not pattern_present:
            with open(gitignore, 'a') as fd:
                fd.write("\n%s" % pattern)

    def create(self):
        if os.path.isdir(self.repo_dir):
            # TODO: check if repo_dir is a git repo and scm_url matches with one of the remotes
            return
        else:
            os.makedirs(self.repo_dir)

        scm_url = utils.get_scm_url(self.pw_url, self.pw_project)

        cmds = [ {'cmd': ['git', 'clone', scm_url, self.repo_dir] }
        ]
        print 'Cloning the repo'
        if not utils.all_succeed(self._exec(cmds)):
            raise RepoException(self.series, self.revision, self.repo_dir, verb="create")

    def config(self):
        # include the poll timestamp file into .gitignore so it is
        # not remove when git clean
        self._add_gitignore(".git-pw.%s.poll.timestamp" % self.pw_project)

        # TODO: we should check if the following are present, so we do not
        # overwrite it each time
        cmds = [
            {'cmd':['git', 'config', 'patchwork.default.url', self.pw_url]},
            {'cmd':['git', 'config', 'patchwork.default.project', self.pw_project]},
            {'cmd':['git', 'config', 'patchwork.default.user', self.pw_user]},
            {'cmd':['git', 'config', 'patchwork.default.password', self.pw_pass]},
        ]

        if not utils.all_succeed(self._exec(cmds)):
            raise RepoException(self.series, self.revision, self.repo_dir, verb="configure")

    def clean(self, remove_branch=False):
        cmds = [
            {'cmd':['git', 'am', '--abort'], "ignore_error":True},
            {'cmd':['git', 'reset', '--hard']},
            {'cmd':['git', 'clean', '-fd']},
            {'cmd':['git', 'checkout', self.stable_branch]},
        ]

        if remove_branch:
            cmds.append({'cmd':['git', 'branch', '-D', self.branch_name]})

        if not utils.all_succeed(self._exec(cmds)):
            raise RepoException(self.series, self.revision, self.repo_dir, verb="clean")

    def fetch(self):
        cmds = [
            {'cmd':['git', 'fetch', "%s" % self.remote]},
        ]
        if not utils.all_succeed(self._exec(cmds)):
            raise RepoException(self.series, self.revision, self.repo_dir, verb="fetch")

    def branch(self):
        cmds = [
            {'cmd':['git', 'checkout', '%s/%s' % (self.remote, self.stable_branch)]},
            {'cmd':['git', 'branch', '-D', self.branch_name], "ignore_error":True},
            {'cmd':['git', 'checkout', '-b', self.branch_name, '%s/%s' % (self.remote, self.stable_branch)]},
        ]

        if not utils.all_succeed(self._exec(cmds)):
            raise RepoException(self.series, self.revision, self.repo_dir, verb="branch")

    def patch(self):
        cmds = [
            {'cmd':['git', 'pw', 'mbox', self.series, '-r', self.revision]},
            {'cmd':['git', 'pw', 'apply', self.series, '-r', self.revision]},
        ]

        if not utils.all_succeed(self._exec(cmds)):
            mbox_url = utils.get_mbox_url(self.pw_url, self.series, self.revision)
            commit_id = utils.get_commit_id('HEAD', self.repo_dir)
            custom_msg = "The series/revision cannot be merge on a top of %s/%s/%s" % (self.remote,
                                                                                       self.stable_branch, 
                                                                                       commit_id)
            # raise RepoPachException, not RepoException, so we can differenciate between
            # patch and non-patch exceptions
            raise RepoPatchException(self.series, self.revision, self.repo_dir, custom_msg=custom_msg)

