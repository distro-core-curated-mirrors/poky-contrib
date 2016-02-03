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

        self._series_revision = self._get_series_revisions(series, revision)


        # for debugging purposes, print all repo parameters
        logger.debug("Parameters")
        logger.debug("\tRepository: %s" % self._repodir)
        logger.debug("\tCommit: %s" % self._commit)
        logger.debug("\tBranch: %s" % self._branch)
        logger.debug("\tMBOX: %s" % self._mbox)
        logger.debug("\tSeries/Revision: %s" % self._series_revision)

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
        elif self._series_revision:
            fullurl = "%s/api/1.0/series/%s/revisions/%s/mbox/"
            _item = [fullurl % (self._url, s,r) for s,r in self._series_revision]
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
            _name += "-local-mbox"
        elif self._series_revision:
            series   = '-'.join([str(s) for s,_ in self._series_revision])
            revision = '-'.join([str(r) for _,r in self._series_revision])
            _name += "-series-%s-rev-%s" % (series, revision)
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

    def _get_series_revisions(self, listseries, listrevisions, defaultrev=1):
        res = []

        logger.debug("listseries %s" % listseries)
        logger.debug("listrevisions %s" % listrevisions)

        # if listseries is falsie, there is nothing to do
        if not listseries:
            return res

        if not listrevisions:
            # if listrevisions is falsie, we need to get the latest revisions
            logger.debug("INSIDE")
            for series in listseries:
                url = "%s/api/1.0/series/%s" % (self._url, series)
                try:
                    r = requests.get(url)
                    rjson = r.json()
                    revision = rjson['version']
                    res.append((series, revision))
                except Exception:
                    logger.warn("latest series' revision could not be obtained from patchwork, using default revision %s" %
                                defaultrev)
                    res.append((series,defaultrev))
        else:
            # TODO: system should also handle the case where:
            res = zip(listseries, listrevisions)
            if len(listseries) != len(listrevisions):
                logger.warn("The number of series and revisions are different, just taking into account:")
                for series, revision in res:
                    logger.warn("\tSeries %s Revision %s" % (series, revision))

        return res

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

    def _check_apply(self, series_revision=None, mbox=None):

        # nothing to check, so return immediately
        if not (series_revision or mbox):
            return

        mbox_data = None
        # get the mbox
        if series_revision:
            series, revision  = series_revision
            mbox_cmd = {'cmd':['git', 'pw', 'mbox', series, '-r', revision], 'strip':False}
            mbox = self._exec(mbox_cmd)[0]
            mbox_data = mbox['stdout']
        elif mbox:
            if not os.path.isfile(mbox):
                raise PatchException, 'mbox %s does not exist' % mbox
            with open(mbox) as mbox_fd:
                mbox_data = mbox_fd.read()

        logger.debug(mbox_data)

        # check if applies
        apply_check_cmd = {'cmd':['git', 'apply', '--check'], 'input':mbox_data}
        self._exec(apply_check_cmd)

    def _apply(self, forcepatch):

        # in case there is neither mbox or series, just return
        if not (self._mbox or self._series_revision):
            return

        # if stashed, then apply these changes before applying
        if self._stashed:
            logger.warning('Applying mbox with stashed data')
            self._exec({'cmd':['git', 'stash', 'apply', self.stashname]})

        items = []
        if self._mbox:
            items = self._mbox
        elif self._series_revision:
            items = self._series_revision

        # check if mbox applies
        for item in items:
            msg = None
            try:
                cmd = None
                if self._mbox:
                    self._check_apply(mbox=item)
                    msg = "The mbox %s" % item
                    cmd = {'cmd':['git', 'am', item]}
                elif self._series_revision:
                    msg = "The series/revision %s/%s" % item
                    self._check_apply(series_revision=item)
                    series, revision = item
                    cmd = {'cmd':['git', 'pw', 'apply', series, '-r', revision]}
                if cmd:
                    self._exec(cmd)
                    logger.info("%s applied" % msg)
            except utils.CmdException as ce:
                if forcepatch:
                    raise PatchException, "%s cannot be applied" % msg
                else:
                    logger.warn("%s cannot be applied, ignoring it" % msg)

    def setup(self, nopatch=False, forcepatch=False):
        if nopatch:
            return

        self._stash()
        self._checkout()
        self._apply(forcepatch)

    def clean(self, nopatch=False, keepbranch=False):
        if nopatch:
            return

        self._destash()
        self._removebranch(keepbranch)

    def post(self, testname, state, summary):
        # TODO: for the moment, all elements on self._series_revision share the same
        # result. System should post independent results for each _series_revision
        for series, revision in self._series_revision:
            cmd = {'cmd':['git', 'pw', 'post-result',
                          series,
                          testname,
                          state,
                          '--summary', summary,
                          '--revision', revision]}
            try:
                self._exec(cmd)
            except utils.CmdException:
                raise RepoException, 'POST requests cannot be done to %s' % self._url

