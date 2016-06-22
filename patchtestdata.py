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

# Data store commonly used to share values between pre and post-merge tests
PatchTestDataStore = collections.defaultdict(str)

class PatchTestStdIn(object):
    """ Generate PatchTestData from standard input"""
    @classmethod
    def namespace_stdin(cls, inputlines):
        cls.series = []
        cls.revision = []
        cls.mbox = []
        for line in inputlines:
            try:
                obj = json.loads(line)
                series, revision = cls.get_series_revision(obj)
                if series and revision:
                    cls.series.append(series)
                    cls.revision.append(revision)
            except ValueError:
                # we try the input as a mbox path
                mbox_path = line.strip()
                if mbox_path:
                    cls.mbox.append(mbox_path)

    @classmethod
    def get_series_revision(cls, obj):
        # variables to hold possible series/revision ids
        series, revision = None, None

        if not obj:
            return series, revision

        # json objects ared different depending on the git pw subcommand
        if obj.has_key('series'):
            # this is an event (git pw poll-events)
            if obj.has_key('parameters'):
                if obj['parameters'].has_key('revision'):
                    series, revision = obj['series'], obj['parameters']['revision']
        elif obj.has_key('id'):
            # this is a series (git pw list -j)
            if obj.has_key('version'):
                series, revision = obj['id'], obj['version']

        return series, revision

class PatchTestArgs(object):
    """ Generate PatchTestData from an argument parser"""

    @classmethod
    def set_namespace(cls):
        parser = cls.get_parser()
        parser.parse_args(namespace=cls)

    @classmethod
    def get_parser(cls):
        parser = argparse.ArgumentParser()

        parser.add_argument('patch', metavar='PATCH',
                            help='The patch to be tested by patchtest')

        parser.add_argument('--post-submitters', '-p',
                            dest='post_submitters',
                            default='',
                            help="Regular expression that indicated the submitters that patchtest can POST")

        parser.add_argument('-C',
                            dest='repodir',
                            default=os.getcwd(),
                            help="Name of the repository where testing is done")

        parser.add_argument('--test-name',
                            dest='testname',
                            default='patchtest',
                            help="Test name to be used if results are posted. In case all items failed merged, then the test name is <--test-name>-merge-failure")

        # Keeps --keep-branch and --no-post mutually exclusive
        branch_group = parser.add_mutually_exclusive_group()

        branch_group.add_argument('--keep-branch',
                                  dest='keepbranch',
                                  action='store_true',
                                  help="Keep the working branch after patchtest execution")

        branch_group.add_argument('--no-patch',
                                  dest='nopatch',
                                  action='store_true',
                                  help="Do not patch the mbox/series")

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

        parser.add_argument('--quiet', '-q',
                            action='store_true',
                            help='Print only errors')

        parser.add_argument('--print-failure-value',
                            action='store_true',
                            dest='print_values',
                            help='Print only errors')


        return parser

# Class used as a namespace to share data from patchtest to the test suites
class PatchTestInput(PatchTestArgs, PatchTestStdIn):
    """ PatchTest wrapper input class"""
    pass
