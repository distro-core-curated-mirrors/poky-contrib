#!/usr/bin/env python
#
# The only purpose of this module is to pass data from patchtest to
# the test suites (PatchTestInput) and between test suites (PatchTestDataStore).

# Strictly speaking, unit test should be isolated from outside,
# but patchtest test suites uses command line input data (series, mboxes,
# etc).

import os
import argparse
import json
import collections
from tempfile import mkstemp
import logging

logger=logging.getLogger('patchtest')
info=logger.info

# Data store commonly used to share values between pre and post-merge tests
PatchTestDataStore = collections.defaultdict(str)

class PatchTestStdIn(object):
    """Gather patch data from standard input"""

    @classmethod
    def namespace_stdin(cls, inputlines):
        (_, patch) = mkstemp()
        with open(patch,'w') as patchfd:
            for line in inputlines:
                patchfd.write(line)
        return patch

class PatchTestArgs(object):
    """Abstract the patchtest argument parser"""

    @classmethod
    def set_namespace(cls):
        parser = cls.get_parser()
        parser.parse_args(namespace=cls)

    @classmethod
    def get_parser(cls):
        parser = argparse.ArgumentParser()

        parser.add_argument('patch', metavar='PATCH',
                            help='The patch to be tested by patchtest')

        parser.add_argument('-C',
                            dest='repodir',
                            default=os.getcwd(),
                            help="Name of the repository where testing is done")

        parser.add_argument('--test-name',
                            dest='testname',
                            default='patchtest',
                            help="Test name to be used if results are posted. In case all items failed merged, then the test name is <--test-name>-merge-failure")

        branch_group = parser.add_mutually_exclusive_group()

        branch_group.add_argument('--keep-branch',
                                  dest='keepbranch',
                                  action='store_true',
                                  help="Keep the working branch after patchtest execution")

        branch_group.add_argument('--no-apply',
                                  dest='noapply',
                                  action='store_true',
                                  help="Do not apply the patch into the repo")

        patchtest_tests_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests')
        parser.add_argument('--test-dir',
                            dest='testdir',
                            default=patchtest_tests_dir,
                            help="Directory where tests are located")

        parser.add_argument('--branch', '-b',
                            dest='branch',
                            help="Branch name used by patchtest to branch from. By default, it uses the current one.")

        parser.add_argument('--commit', '-c',
                            dest='commit',
                            help="Commit ID used by patchtest to branch from. By default, it uses HEAD.")

        parser.add_argument('--debug', '-d',
                            action='store_true',
                            help='Enable debug output')

        parser.add_argument('--failures', '-f',
                            action='store_true',
                            dest='pfailures',
                            help='Print just failures')

        parser.add_argument('--raw', '-r',
                            action='store_true',
                            dest='raw',
                            help='Print errors coming from the test suite')


        return parser

# Class used as a namespace to share data from patchtest to the test suites
class PatchTestInput(PatchTestArgs, PatchTestStdIn):
    """ PatchTest wrapper input class"""
    pass
