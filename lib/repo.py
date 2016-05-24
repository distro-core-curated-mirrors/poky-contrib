import os
import utils
import git
import logging
import requests
import json
from mboxitem import MboxItem, MboxURLItem, MboxFileItem

logger = logging.getLogger('patchtest')

class Repo(object):

    # prefixes used for temporal branches/stashes
    prefix = 'patchtest'

    def __init__(self, repodir, commit=None, branch=None, mbox=None, series=None, revision=None):
        self._repodir = repodir
        self._mbox = mbox

        # check if repo is controlled by GIT
        try:
            self.repo = git.Repo(self._repodir)
        except git.exc.InvalidGitRepositoryError:
            logger.error('Not a git repository')
            raise Exception

        config = self.repo.config_reader()

        # check if git-pw config is present
        try:
            patchwork_section = 'patchwork "%s"' % 'default'
            self._url = config.get(patchwork_section, 'url')
            self._project = config.get(patchwork_section, 'project')
        except:
            logger.error('patchwork url/project configuration is not available')
            raise Exception

        # check patchwork instance is alive
        try:
            requests.get("%s/api/1.0" % self._url)
        except:
            logger.error('patchwork instance is not alive: %s' % self._url)
            raise Exception

        self._series_revision = self._get_series_revisions(series, revision)

        # create the items
        self._mboxitems = self._create_items()

        # get current branch name, so we can checkout at the end
        self._current_branch = self._get_current_branch()

        # branch to be used for testing, priority: branch provided by
        # user, branch defined in item/items or current branch
        self._branch = branch or self._get_items_branch() or self._current_branch
        self._commit = self._get_commitid(commit or self._branch)
        self._branchname = "%s_%s" % (Repo.prefix, os.getpid())
        self._mailinglist = self._get_mailinglist()

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

    @property
    def mailinglist(self):
        return self._mailinglist

    @property
    def branch(self):
        return self._branch

    @property
    def commit(self):
        return self._commit

    def _get_mailinglist(self, defaultml=''):
        ml = defaultml
        url = "%s/api/1.0/projects/%s" % (self._url, self._project)
        try:
            r = requests.get(url)
            ml = r.json()['listemail']
        except Exception as e:
            logger.warn("Mailing list could not be fetched")
        return ml

    def _create_items(self):
        """ Load MboxItems to be tested """
        _mboxitems = []
        if self._mbox:
            for _eachitem in self._mbox:
                _mboxitems.append(MboxFileItem(_eachitem))
        elif self._series_revision:
            fullurl = "%s" % self._url
            fullurl +="/api/1.0/series/%s/revisions/%s/mbox/"
            for s,r in self._series_revision:
                _mboxitems.append(MboxURLItem(fullurl, (s,r)))
        return _mboxitems

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

    def _get_current_branch(self, commit='HEAD'):
        cmd = {'cmd':['git', 'rev-parse', '--abbrev-ref', commit]}
        return self._exec(cmd)[0]['stdout']

    def _get_items_branch(self):
        branch = None
        branches = [b.getbranch() for b in self._mboxitems]
        if branches and all(branches):
            head, tail = branches[0], branches[1:]
            if tail:
                # in case of multiple items, all items should target
                # the same branch
                if all(map(lambda b: head == b, tail)):
                    branch = head
            else:
                branch = head

        if branch:
            logger.debug('branch name detected on mbox: %s' % branch)
            # now check if the branch that the item is refering to actually exists on the repo
            res = self._exec({'cmd':['git', 'branch', '--remote', '--list', '*/%s' % branch]})
            remote_branch = res[0]['stdout']
            if remote_branch:
                logger.debug('Remote branch to be used: %s' % remote_branch)
                branch = remote_branch
            else:
                branch = None

        return branch

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

    def _merge_item(self, item):
        contents = item.contents

        if not contents:
            logger.error('Contents are empty')
            raise Exception

        self._exec([
            {'cmd':['git', 'apply', '--check', '--verbose'], 'input':contents},
            {'cmd':['git', 'am'], 'input':contents, 'updateenv':{'PTRESOURCE':item.resource}}]
        )

    def merge(self):
        # create the branch before merging
        self._exec([
            {'cmd':['git', 'checkout', self._branch]},
            {'cmd':['git', 'checkout', '-b', self._branchname, self._commit]},
        ])

        # merge the items
        for item in self._mboxitems:
            try:
                self._merge_item(item)
                item.status = MboxItem.MERGE_STATUS_MERGED_SUCCESSFULL
            except utils.CmdException as ce:
                item.status = MboxItem.MERGE_STATUS_MERGED_FAIL
            except:
                item.status = MboxItem.MERGE_STATUS_INVALID

    def any_merge(self):
        for item in self._mboxitems:
            if item.status == MboxItem.MERGE_STATUS_MERGED_SUCCESSFULL:
                return True
        return False

    def clean(self, keepbranch=False):
        """ Leaves the repo as it was before testing """
        cmds = [
            {'cmd':['git', 'checkout', '%s' % self._current_branch]},
        ]

        if not keepbranch:
            cmds.append({'cmd':['git', 'branch', '-D', self._branchname], 'ignore_error':True})

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
                logger.warn('POST requests cannot be done to %s' % self._url)

