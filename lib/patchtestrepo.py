#!/usr/bin/python
# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
# patchtestrepo: Repo class used mainly to control a git repo from patchtest
#
# Copyright (C) 2016 Intel Corporation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

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

        self._branch = self._get_commitid(branch) or \
                       self._get_commitid(self._patch.branch) or \
                       self._current_branch

        self._commit = self._get_commitid(commit) or \
                       self._get_commitid('HEAD')

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

    def _get_commitid(self, commit):

        if not commit:
            return None

        try:
            cmd = {'cmd':['git', 'rev-parse', '--short', commit]}
            return self._exec(cmd)[0]['stdout']
        except utils.CmdException as ce:
            # try getting the commit under any remotes
            cmd = {'cmd':['git', 'remote']}
            remotes = self._exec(cmd)[0]['stdout']
            for remote in remotes.splitlines():
                cmd = {'cmd':['git', 'rev-parse', '--short', '%s/%s' % (remote, commit)]}
                try:
                    return self._exec(cmd)[0]['stdout']
                except utils.CmdException:
                    pass

        return None

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
