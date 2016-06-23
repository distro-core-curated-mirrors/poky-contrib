import os
import utils
import git
import logging
import requests
import json
from patchtestpatch import Patch

logger = logging.getLogger('patchtest')
info=logger.info

class Repo(object):

    # prefixes used for temporal branches/stashes
    prefix = 'patchtest'

    def __init__(self, patch, repodir, commit=None, branch=None):
        self._repodir = repodir
        self._patch = Patch(patch)
        self._current_branch = self._get_current_branch()

        # branch to be used for testing, priority: branch provided by
        # user, branch defined in item/items or current branch
        self._branch = branch or self._patch.branch or self._current_branch
        self._commit = self._get_commitid(commit or self._branch)
        self._branchname = "%s_%s" % (Repo.prefix, os.getpid())

        # for debugging purposes, print all repo parameters
        logger.debug("Parameters")
        logger.debug("\tRepository: %s" % self._repodir)
        logger.debug("\tCommit: %s" % self._commit)
        logger.debug("\tBranch: %s" % self._branch)
        logger.debug("\tPatch: %s" % self._patch)

    @property
    def patch(self):
        return self._patch.path

    @property
    def branch(self):
        return self._branch

    @property
    def commit(self):
        return self._commit

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

    def _get_commitid(self, commit='HEAD'):
        out = None
        try:
            cmd = {'cmd':['git', 'rev-parse', '--short', commit]}
            out = self._exec(cmd)[0]['stdout']
        except utils.CmdException as ce:
            # try getting the commit under any remotes
            cmd = {'cmd':['git', 'remote']}
            remotes = self._exec(cmd)[0]['stdout']
            for remote in remotes.splitlines():
                cmd = {'cmd':['git', 'rev-parse', '--short', '%s/%s' % (remote, commit)]}
                try:
                    out = self._exec(cmd)[0]['stdout']
                    break
                except:
                    pass
            else:
                logger.error('commit (%s) not found on any remote')

        return out

    def merge(self):
        # create the branch before merging
        self._exec([
            {'cmd':['git', 'checkout', self._branch]},
            {'cmd':['git', 'checkout', '-b', self._branchname, self._commit]},
        ])

        if not self._patch.contents:
            logger.error('Contents are empty')
            raise Exception
        try:
            self._exec([
                {'cmd':['git', 'apply', '--check', '--verbose'], 'input':self._patch.contents},
                {'cmd':['git', 'am'], 'input':self._patch.contents, 'updateenv':{'PTRESOURCE':self._patch.path}}]
                )
            self._patch.merge_status = Patch.MERGE_STATUS_MERGED_SUCCESSFULL
        except utils.CmdException as ce:
            self._patch.merge_status = Patch.MERGE_STATUS_MERGED_FAIL
        except Exception as e:
            self._patch.merge_status = Patch.MERGE_STATUS_INVALID

        return self._patch.merge_status == Patch.MERGE_STATUS_MERGED_SUCCESSFULL

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

