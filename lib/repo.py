import os
import utils
import git
import logging
import requests

logger = logging.getLogger('patchtest')

class RepoException(Exception):
    pass

class BaseMboxItem(object):
    """ mbox item containing all data extracted from an mbox, and methods
        to extract this data. This base class and should be inherited
        from, not directly instantiated.
    """
    MERGE_STATUS_INVALID = 'INVALID'
    MERGE_STATUS_NOT_MERGED = 'NOTMERGED'
    MERGE_STATUS_MERGED_SUCCESSFULL = 'PASS'
    MERGE_STATUS_MERGED_FAIL = 'FAIL'
    MERGE_STATUS = (MERGE_STATUS_INVALID,
                    MERGE_STATUS_NOT_MERGED,
                    MERGE_STATUS_MERGED_SUCCESSFULL,
                    MERGE_STATUS_MERGED_FAIL)

    def __init__(self, resource, args=None, forcereload=False):
        self._resource = resource
        self._args = args
        self._forcereload = forcereload

        self._contents = ''
        self._status = BaseMboxItem.MERGE_STATUS_NOT_MERGED

    @property
    def contents(self):
        raise(NotImplementedError, 'Please do not instantiate MboxItem')

    def _scan(self):
        raise(NotImplementedError, 'This method has not yet been implemented, scanning is done in tests')

    @property
    def is_empty(self):
        return not self.contents

    def getresource(self):
        resource = self._resource
        if self._args:
            resource %= self._args
        return resource

    def setresource(self, resouce):
        self._resource = resource

    resource = property(getresource, setresource)

    def getargs(self):
        return self._args

    def setargs(self, args):
        self._args = args

    args = property(getargs, setargs)

    def getstatus(self):
        return self._status

    def setstatus(self, status):
        if not status in BaseMboxItem.MERGE_STATUS:
            logger.warn('Status (%s) not valid' % status)
        else:
            self._status = status

    status = property(getstatus, setstatus)

class MboxURLItem(BaseMboxItem):
    """ mbox item based on a URL"""

    @property
    def contents(self):
        if self._forcereload or (not self._contents):
            logger.debug('Reading %s contents' % self.resource)
            try:
                _r = requests.get(self.resource)
                self._contents = _r.text
            except:
                logger.warn("Request to %s failed" % self.resource)
        return self._contents

class MboxFileItem(BaseMboxItem):
    """ mbox item based on a file"""

    @property
    def contents(self):
        if self._forcereload or (not self._contents):
            logger.debug('Reading %s contents' % self.resource)
            try:
                with open(self.resource) as _f:
                    self._contents = _f.read()
            except IOError:
                logger.warn("Reading the mbox %s failed" % self.resource)
        return self._contents

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
            fullurl = "%s" % self._url
            fullurl +="/api/1.0/series/%s/revisions/%s/mbox/"
            for s,r in self._series_revision:
                self._mboxitems.append(MboxURLItem(fullurl, (s,r)))

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
        except utils.CmdException as ce:
            cmd = ' '.join(ce.cmd)
            logger.error("CMD: %s" % cmd)
            logger.debug("CMD: %s RCODE: %s STDOUT: %s STDERR: %s" %
                         (cmd, ce.returncode, ce.stdout, ce.stderr))
            raise ce

        if logger.getEffectiveLevel() == logging.DEBUG:
            for result in results:
                logger.debug("CMD: %s RCODE: %s STDOUT: %s STDERR: %s" %
                             (' '.join(result['cmd']), result['returncode'], result['stdout'], result['stderr']))

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

    def _store_mbox(self, item):
        if isinstance(item, MboxURLItem):
            series, revision = item.args
            mbox_file = "series-%s-revision-%s.mbox" % (series, revision)
            logger.info('Storing mbox/series into %s' % os.path.abspath(mbox_file))
            with open(mbox_file, 'w') as f:
                f.write(item.contents)

    def _merge_item(self, item):
        contents = item.contents
        if not contents:
            raise Exception('Contents are empty')

        self._exec([
            {'cmd':['git', 'apply', '--check', '--verbose'], 'input':contents},
            {'cmd':['git', 'am'], 'input':contents}]
        )

    def merge(self, storembox=False):
        for item in self._mboxitems:
            if storembox:
                self._store_mbox(item)
            try:
                self._merge_item(item)
                item.status = BaseMboxItem.MERGE_STATUS_MERGED_SUCCESSFULL
            except utils.CmdException as ce:
                item.status = BaseMboxItem.MERGE_STATUS_MERGED_FAIL
            except:
                item.status = BaseMboxItem.MERGE_STATUS_INVALID

    def any_merge(self):
        for item in self._mboxitems:
            if item.status == BaseMboxItem.MERGE_STATUS_MERGED_SUCCESSFULL:
                return True
        return False

    def setup(self):
        """ Setup repository for patching """
        self._exec([
            {'cmd':['git', 'stash', 'save']},
            {'cmd':['git', 'checkout', self.branch]},
            {'cmd':['git', 'checkout', '-b', self.branchname, self.commit]},
        ])

    def clean(self, keepbranch=False):
        """ Leaves the repo as it was before testing """
        cmds = [
            {'cmd':['git', 'checkout', '%s' % self._current_branch]},
            {'cmd':['git', 'stash', 'pop'], 'ignore_error':True},
        ]

        if not keepbranch:
            cmds.append({'cmd':['git', 'branch', '-D', self.branchname], 'ignore_error':True})

        self._exec(cmds)

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

