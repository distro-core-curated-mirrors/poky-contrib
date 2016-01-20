import inspect
import os
import utils
import git
import logging

logger = logging.getLogger('patchtest')

class RepoException(Exception):
    pass

class PatchException(Exception):
    pass

class Repo(object):

    # prefixes used for branches and temp directory
    branchnameprefix = 'patchtest'
    tempdirprefix = 'patchtest'

    def __init__(self, commit, branch, mbox, series, revision, repodir):

        self._commit = commit
        self._branch = branch
        self._mbox = mbox
        self._series = series
        self._revision = revision
        self._repodir = repodir

        self._stashed = False
        self._current_branch, self._current_commit = self._get_current_branch_commit()

        try:
            self.repo = git.Repo(self._repodir)
        except git.exc.InvalidGitRepositoryError:
            logger.error('Not a git repository')
            raise RepoException

        config = self.repo.config_reader()

        try:
            patchwork_section = 'patchwork "%s"' % 'default'
            self._url = config.get(patchwork_section, 'url')
            self._project = config.get(patchwork_section, 'project')
        except:
            logger.error('patchwork url/project configuration is not available')
            raise RepoException

    @property
    def mbox(self):
        mbox = ''
        if self._mbox:
            mbox = self._mbox
        elif self._series and self._revision:
            mbox = "%s/api/1.0/series/%s/revisions/%s/mbox/" % (self._url, self._series, self._revision)
        return mbox

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
        _cmds = []
        if isinstance(cmds, dict):
            _cmds.append(cmds)
        elif isinstance(cmds, list):
            _cmds = cmds
        else:
            logger.error('Unknown cmd format')
            raise RepoException

        try:
            results = utils.exec_cmds(_cmds, self._repodir)
        except utils.CmdException as ce:
            logger.error(ce)
            raise RepoException

        if logger.getEffectiveLevel() == logging.DEBUG:
            for result in results:
                logger.debug(result)

        return results

    def _get_current_branch_commit(self):
        branch = None
        commit = None
        # before branching, save current branch/commit
        cmds = [ {'cmd':['git', 'rev-parse', '--abbrev-ref', 'HEAD']},
                 {'cmd':['git', 'rev-parse', 'HEAD']},
        ]
        results = self._exec(cmds)
        if results:
            branch = results[0]['stdout']
            commit = results[1]['stdout']

        return (branch, commit)

    def _apply_abort(self):
        self._exec({'cmd':['git', 'am', '--abort'], 'ignore_error':True})

    def _stash(self):
        # check first if repository is dirty
        dirty = self._exec({'cmd':['git', 'diff', '--shortstat']}) [0]['stdout']
        if dirty:
            self._exec({'cmd':['git', 'stash']})
            self._stashed = True

    def _destash(self):
        cmds = [{'cmd':['git', 'checkout', '%s' % self._current_branch]}]

        if self._stashed:
            cmds.append({'cmd':['git', 'stash', 'apply']})
            self._stashed = False

        self._exec(cmds)

    def _removebranch(self, keepbranch):
        if not keepbranch:
            self._exec({'cmd':['git', 'branch', '-D', self.branchname]})

    def _checkout(self):
        cmds = [
            {'cmd':['git', 'checkout', self.branch]},
            {'cmd':['git', 'checkout', '-b', self.branchname, self.commit], 'ignore_error':True},
        ]
        self._exec(cmds)

    def _apply(self):
        cmd = None
        if self._mbox:
            cmd = {'cmd':['git', 'am', self._mbox]}
        elif self._series:
            cmd = {'cmd':['git', 'pw', 'apply', self._series, '-r', self._revision]}

        if cmd:
            try:
                self._exec(cmd)
            except RepoException:
                msg = "\nThe mbox \n\n\t%s\n\ncannot be applied on top of %s/%s" % (self.mbox, self.branch, self.commit)
                raise PatchException, msg

    def setup(self):
        self._stash()
        self._checkout()
        self._apply()

    def clean(self, keepbranch=False):
        # calling _apply_abort is neccessary in case the mbox did not apply,
        # so the working directory would be dirty
        self._apply_abort()

        self._destash()
        self._removebranch(keepbranch)

    def post(self, testname, state, summary):
        cmd = {'cmd':['git', 'pw', 'post-result',
                      self._series,
                      testname,
                      state,
                      '--summary', summary,
                      '--revision', self._revision]}
        try:
            self._exec(cmd)
        except RepoException:
            logger.error('POST requests cannot be done to %s' % self._url)
            raise RepoException

