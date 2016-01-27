import os
import utils
import git
import logging
import requests

logger = logging.getLogger('patchtest')

class RepoException(Exception):
    pass

class PatchException(Exception):
    pass

class Repo(object):

    # prefixes used for temporal branches/stashes
    prefix = 'patchtest'

    def __init__(self, repodir, commit=None, branch=None, mbox=None, series=None, revision=None):
        self._repodir = repodir
        self._commit = commit
        self._branch = branch
        self._mbox = mbox
        self._series = series

        self._stashed = False

        # get current branch name, so we can checkout at the end
        self._current_branch = self._get_branch()

        # get user branch name and commit id, if not given
        # current branch and HEAD is take
        self._branch = branch or self._current_branch
        self._commit = self._get_commitid(commit or 'HEAD')

        try:
            self.repo = git.Repo(self._repodir)
        except git.exc.InvalidGitRepositoryError:
            raise RepoException, 'Not a git repository'

        config = self.repo.config_reader()

        try:
            patchwork_section = 'patchwork "%s"' % 'default'
            self._url = config.get(patchwork_section, 'url')
            self._project = config.get(patchwork_section, 'project')
        except:
            raise RepoException, 'patchwork url/project configuration is not available'

        # Revision is optional. If not present, get the latest from patchwork
        self._revision = series and (revision or self._get_latest_rev(series))

        # for debugging purposes, print all repo parameters
        logger.debug("Parameters")
        logger.debug("\tRepository: %s" % self._repodir)
        logger.debug("\tCommit: %s" % self._commit)
        logger.debug("\tBranch: %s" % self._branch)
        logger.debug("\tMBOX: %s" % self._mbox)
        logger.debug("\tSeries: %s" % self._series)
        logger.debug("\tRevision: %s" % self._revision)

    @property
    def url(self):
        return self._url

    @property
    def project(self):
        return self._project

    @property
    def item(self):
        """ Item to be tested """
        _item = ''
        if self._mbox:
            _item = self._mbox
        elif self._series:
            _item = "%s/api/1.0/series/%s/revisions/%s/mbox/" % (self._url, self._series, self._revision)
        else:
            _item = "%s/%s" % (self._branch, self._commit)
        return _item

    @property
    def branch(self):
        return self._branch

    @property
    def commit(self):
        return self._commit

    @property
    def branchname(self):
        _name = Repo.prefix
        if self._mbox:
            # patchtest-local-mbox
            _name += "-local-mbox"
        elif self._series:
            # patchtest-series-<series>-rev-<revision>
            _name += "-series-%s-rev-%s" % (self._series, self._revision)
        return _name

    @property
    def stashname(self):
        return "%s-%s-%s" % (Repo.prefix, self.branch, self.commit)

    def _exec(self, cmds):
        _cmds = []
        if isinstance(cmds, dict):
            _cmds.append(cmds)
        elif isinstance(cmds, list):
            _cmds = cmds
        else:
            raise utils.CmdException({'cmd':str(cmds)})

        results = []
        try:
            results = utils.exec_cmds(_cmds, self._repodir)
        finally:
            if logger.getEffectiveLevel() == logging.DEBUG:
                for result in results:
                    logger.debug("CMD: %s" % ' '.join(result['cmd']))

        return results

    def _get_branch(self, commit='HEAD'):
        cmd = {'cmd':['git', 'rev-parse', '--abbrev-ref', commit]}
        return self._exec(cmd)[0]['stdout']

    def _get_commitid(self, commit='HEAD'):
        cmd = {'cmd':['git', 'rev-parse', '--short', commit]}
        return self._exec(cmd)[0]['stdout']

    def _get_latest_rev(self, series):
        revision = 1
        if series:
            url = "%s/api/1.0/series/%s" % (self._url, self._series)
            logger.debug(url)
            try:
                r = requests.get(url)
                rjson = r.json()
                revision = rjson['version']
            except Exception:
                logger.warn("latest series' revision could not be obtained from patchwork, using rev 1")
        return revision

    def _stash(self):
        # stash just when working dir is dirty
        dirty = self._exec({'cmd':['git', 'diff', '--shortstat']}) [0]['stdout']
        if dirty:
            self._exec({'cmd':['git', 'stash', 'save', self.stashname]})
            self._stashed = True

    def _destash(self):
        cmds = [{'cmd':['git', 'checkout', '%s' % self._current_branch]}]

        if self._stashed:
            cmds.append({'cmd':['git', 'stash', 'apply', self.stashname]})
            cmds.append({'cmd':['git', 'stash', 'drop', self.stashname]})
            self._stashed = False

        self._exec(cmds)

    def _removebranch(self, keepbranch):
        if not keepbranch:
            # it may be the case that the branch was not created, so ignore error if not present
            self._exec({'cmd':['git', 'branch', '-D', self.branchname], 'ignore_error':True})

    def _checkout(self):
        cmds = [{'cmd':['git', 'checkout', '-b', self.branchname, self.commit]}]

        # move to the branch if user specified a branch different that current one
        if self._branch != self._current_branch:
            cmds.insert(0, {'cmd':['git', 'checkout', self.branch]})
        self._exec(cmds)

    def _check_apply(self):
        mbox_data = None
        # get the mbox
        if self._series:
            mbox_cmd = {'cmd':['git', 'pw', 'mbox', self._series, '-r', self._revision], 'strip':False}
            mbox = self._exec(mbox_cmd)[0]
            mbox_data = mbox['stdout']
        elif self._mbox:
            if not os.path.isfile(self._mbox):
                raise PatchException, 'mbox %s does not exist' % self._mbox
            with open(self._mbox) as mbox_fd:
                mbox_data = mbox_fd.read()
        else:
            # nothing to apply, return
            return True

        # check if applies
        apply_check_cmd = {'cmd':['git', 'apply', '--check'], 'input':mbox_data}
        self._exec(apply_check_cmd)

    def _apply(self):

        # in case there is neither mbox or series, just return
        if not (self._mbox or self._series):
            return

        # if stashed, then apply these changes before applying
        if self._stashed:
            logger.warning('Applying mbox with stashed data')
            self._exec({'cmd':['git', 'stash', 'apply', self.stashname]})

        # check if mbox applies
        try:
            self._check_apply()
        except utils.CmdException as ce:
            mbox = "The mbox %s\n\ncannot be applied on top of %s/%s" % (self.mbox, self.branch, self.commit)
            reason = "Reason:\n\n%s" % ce.stderr
            msg = "\n%s\n\n%s" % (mbox, reason)
            raise PatchException, msg

        # apply the patch
        cmd = None
        if self._mbox:
            cmd = {'cmd':['git', 'am', self._mbox]}
        elif self._series:
            cmd = {'cmd':['git', 'pw', 'apply', self._series, '-r', self._revision]}
        self._exec(cmd)

    def setup(self, nopatch=False):
        if nopatch:
            return

        self._stash()
        self._checkout()
        self._apply()

    def clean(self, keepbranch=False, nopatch=False):
        if nopatch:
            return

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
        except utils.CmdException:
            raise RepoException, 'POST requests cannot be done to %s' % self._url

