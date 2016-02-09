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

class BaseMboxItem(object):
    """ mbox item containing all data extracted from an mbox, and methods
        to extract this data. This base class and should be inherited
        from, not directly instantiated.
    """
    def __init__(self, resource):
        # private vars
        self._resource = resource
        # public vars
        self.contents = []
        self.keyvals = {}
        self.chgfiles = []
        self.patchdiff = ''
        self.hunks = {}
        # load mbox contents
        self._load_contents()

    def _load_contents(self):
        raise(NotImplementedError, 'Please do not instantiate MboxItem')

    def _scan(self):
        raise(NotImplementedError, 'This method has not yet been implemented, scanning is done in tests')

    def __str__(self):
        return "%s" % self._resource

    @property
    def is_empty(self):
        return not( ''.join(self.contents).strip() )

class MboxURLItem(BaseMboxItem):
    """ mbox item based on a URL"""
    def _load_contents(self):
        _r = requests.get(self._resource)
        self.contents = _r.text

class MboxFileItem(BaseMboxItem):
    """ mbox item based on a file"""
    def _load_contents(self):
        with open(os.path.abspath(self._resource)) as _f:
            self.contents = _f.read()

class Repo(object):

    # prefixes used for temporal branches/stashes
    prefix = 'patchtest'

    def __init__(self, repodir, commit=None, branch=None, mbox=None, series=None, revision=None):
        self._repodir = repodir
        self._commit = commit
        self._branch = branch
        self._mbox = mbox
        self._stashed = False
        self._mboxitems = []

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
        self._loaditems()

        # for debugging purposes, print all repo parameters
        logger.debug("Parameters")
        logger.debug("\tRepository: %s" % self._repodir)
        logger.debug("\tCommit: %s" % self._commit)
        logger.debug("\tBranch: %s" % self._branch)
        logger.debug("\tMBOX: %s" % self._mbox)
        logger.debug("\tSeries/Revision: %s" % self._series_revision)

    @property
    def items(self):
        """ Items to be tested. By default it is initialized as an empty list"""
        return self._mboxitems

    @property
    def url(self):
        return self._url

    @property
    def project(self):
        return self._project

    def _loaditems(self):
        """ Load MboxItems to be tested """
        if self._mbox:
            for _eachitem in self._mbox:
                self._mboxitems.append(MboxFileItem(_eachitem))
        elif self._series_revision:
            fullurl = "%s/api/1.0/series/%s/revisions/%s/mbox/"
            for _mbox_url in [fullurl % (self._url, s,r) for s,r in self._series_revision]:
                self._mboxitems.append(MboxURLItem(_mbox_url))

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

    def _fetch_latest_revision(self, series, defaultrev=1):
        revision = None
        url = "%s/api/1.0/series/%s" % (self._url, series)
        try:
            r = requests.get(url)
            rjson = r.json()
            revision = rjson['version']
        except Exception:
            revision = defaultrev
            logger.warn("latest series' revision could not be obtained from patchwork, using default revision %s" %
                        defaultrev)
        return revision

    def _get_series_revisions(self, listseries, listrevisions, defaultrev=1):
        res = []

        if not listseries:
            return res

        if not listrevisions:
            for series in listseries:
                revision = self._fetch_latest_revision(series)
                res.append((series, revision))
        else:
            if len(listseries) != len(listrevisions):
                logger.warn("The number of series and revisions are different")

            for series, revision in zip(listseries, listrevisions):
                if not revision:
                    latest_revision = self._fetch_latest_revision(series)
                    res.append((series, latest_revision))
                else:
                    res.append((series, revision))
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

    def _check_apply(self, series_revision=None, mbox=None, storembox=False):

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
            mbox_file = "series-%s-revision-%s.mbox" % (series, revision)
            if storembox:
                logger.info('Storing mbox/series into %s' % os.path.abspath(mbox_file))
                with open(mbox_file, 'w') as f:
                    f.write(mbox_data)
        elif mbox:
            if not os.path.isfile(mbox):
                raise PatchException, 'mbox %s does not exist' % mbox
            with open(mbox) as mbox_fd:
                mbox_data = mbox_fd.read()

        # check if applies
        apply_check_cmd = {'cmd':['git', 'apply', '--check'], 'input':mbox_data}
        self._exec(apply_check_cmd)

    def _apply(self, forcepatch, storembox):

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
                    self._check_apply(series_revision=item, storembox=storembox)
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

    def setup(self, nopatch=False, forcepatch=False, storembox=False):
        if nopatch:
            return

        self._stash()
        self._checkout()
        self._apply(forcepatch, storembox)

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

