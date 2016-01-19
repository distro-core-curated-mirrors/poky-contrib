import inspect
import os
import utils
import git

class RepoException(Exception):
    pass

class PatchException(Exception):
    pass

class Repo(object):

    # prefixes used for branches and temp directory
    branchnameprefix = 'patchtest'
    tempdirprefix = 'patchtest'

    def __init__(self, commit, branch, mbox, series, revision, repodir, tempbasedir):

        self._commit = commit
        self._branch = branch
        self._mbox = mbox
        self._series = series
        self._revision = revision
        self._repodir = repodir
        self._tempbasedir = tempbasedir

        self._stashed = False
        self._current_branch, self._current_commit = self._get_current_branch_commit()

        try:
            self.repo = git.Repo(self._repodir)
        except git.exc.InvalidGitRepositoryError:
            raise RepoException('Not a git repository.')

        config = self.repo.config_reader()

        try:
            patchwork_section = 'patchwork "%s"' % 'default'
            self._url = config.get(patchwork_section, 'url')
            self._project = config.get(patchwork_section, 'project')
        except:
            raise RepoException('patchwork url/project configuration is not available')

    @property
    def mboxurl(self):
        return "%s/api/1.0/series/%s/revisions/%s/mbox/" % (self._url, self._series, self._revision)

    @property
    def tempdir(self):
        return "%s/%s-%s-%s" % (self._tempbasedir, Repo.tempdirprefix, self._series, self._revision)

    @property
    def branch(self):
        if not self._branch:
            self._branch = self._current_branch
        return self._branch

    @property
    def commit(self):
        if not self._commit:
            self._commit = self._current_commit
        return self._commit

    @property
    def branchname(self):
        return "%s-%s-%s" % (Repo.branchnameprefix, self.branch, self.commit)

    def _exec(self, cmds):
        stack = inspect.stack()
        taskname = stack[1][3]
        return utils.exec_cmds(cmds, self._repodir, self.tempdir, taskname)

    def _get_current_branch_commit(self):
        branch = None
        commit = None
        # before branching, save current branch/commit
        cmds = [ {'cmd':['git', 'rev-parse', '--abbrev-ref', 'HEAD']},
                 {'cmd':['git', 'rev-parse', 'HEAD']},
        ]
        results = utils.exec_cmds(cmds, self._repodir)
        if results:
            branch = results[0]['stdout']
            commit = results[1]['stdout']

        return (branch, commit)

    def _stash(self):
        # check first if repository is dirty
        cmds = [{'cmd':['git', 'diff', '--shortstat']}]
        dirty = utils.exec_cmds(cmds, self._repodir)[0]['stdout']
        if dirty:
            cmds = [{'cmd':['git', 'stash']}]
            if not utils.all_succeed(self._exec(cmds)):
                raise RepoException
            self._stashed = True

    def _destash(self):
        cmds = [{'cmd':['git', 'checkout', '%s' % self._current_branch]}]

        if self._stashed:
            cmds.append({'cmd':['git', 'stash', 'apply']})
            self._stashed = False

        if not utils.all_succeed(self._exec(cmds)):
            raise RepoException

    def _removebranch(self, keepbranch=False):
        cmds = []
        if not keepbranch:
            cmds.append({'cmd':['git', 'branch', '-D', self.branchname]})

        if not utils.all_succeed(self._exec(cmds)):
            raise RepoException

    def _checkout(self):
        cmds = [
            {'cmd':['git', 'checkout', self.branch]},
            {'cmd':['git', 'checkout', '-b', self.branchname, self.commit], 'ignore_error':True},
        ]
        if not utils.all_succeed(self._exec(cmds)):
            raise RepoException('Repo cannot be branched')

    def _apply(self):
        cmds = []
        if self._mbox:
            cmds = [ {'cmd':['git', 'am', self._mbox]} ]
        elif self._series:
            cmds = [ {'cmd':['git', 'pw', 'apply', self._series, '-r', self._revision]} ]

        if cmds:
            if not utils.all_succeed(self._exec(cmds)):
                msg = "The series/revision cannot be applied on top of %s/%s" % (self.branch, self.commit)
                raise PatchException, msg

    def setup(self):
        self._stash()
        self._checkout()
        self._apply()

    def clean(self, keepbranch):
        self._destash()
        self._removebranch(keepbranch)

    def post(self, testname, state, summary):
        cmds = [
            {'cmd':['git', 'pw', 'post-result',
                    self._series,
                    testname,
                    state,
                    '--summary', summary,
                    '--revision', self._revision]},
        ]

        if not utils.all_succeed(self._exec(cmds)):
            raise RepoException('POST requests cannot be done to %s' % self._url)

