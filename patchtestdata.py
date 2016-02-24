#!/usr/bin/env python

import os
import argparse
import json

# This module contains classes to store the command line arguments
# and standard input items passed to the 'patchtest' script. Test
# cases can import it and use it to figure out the values, like
# the repo directory of the current mbox/series being tested.
# See tests/test_sample.py test case for usage examples.

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

        parser.add_argument('--series', '-s',
                            nargs='*',
                            dest='series',
                            default=[],
                            help='The series ids to patch and test. Add --no-patch if no patching is done into the repository')

        parser.add_argument('--revision', '-r',
                            nargs='*',
                            dest='revision',
                            default=[],
                            help='The revisions to patch and test, latest if omitted. Add --no-patch if no patching is done into the repository')

        parser.add_argument('--post',
                            dest='post',
                            action='store_true',
                            help="Post results to patchwork")

        parser.add_argument('--mbox', '-m',
                            nargs='*',
                            dest='mbox',
                            default=[],
                            help='mbox files to patch and test. Add --no-patch if no patching is done into the repository')

        parser.add_argument('-C',
                            dest='repodir',
                            default=os.getcwd(),
                            help="Name of the repository where testing is done")

        parser.add_argument('--test-name',
                            dest='testname',
                            default='patchtest',
                            help="Test name to be used if results are posted")

        parser.add_argument('--keep-branch',
                            dest='keepbranch',
                            action='store_true',
                            help="Do not post results")

        patchtest_tests_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'tests')
        parser.add_argument('--test-dir',
                            dest='testdir',
                            default=patchtest_tests_dir,
                            help="Directory where tests are located")

        parser.add_argument('--branch', '-b',
                            dest='branch',
                            help="Branch to work on, default is master. Must be available in repo")

        parser.add_argument('--commit', '-c',
                            dest='commit',
                            help="Commit to work on, default is HEAD. Must be visible from branch")

        parser.add_argument('--patching-strategy', '-p',
                            dest='patching_strategy',
                            default='single',
                            help="Patching strategy: 'single' test a single patch, 'multiple' test multiple patches , 'no' do not patch, just test")

        parser.add_argument('--store-mbox',
                            dest='storembox',
                            action='store_true',
                            help="Store the mbox/series into a file")

        parser.add_argument('--debug', '-d',
                            action='store_true',
                            help='Enable debug output')

        parser.add_argument('--quiet', '-q',
                            action='store_true',
                            help='Print only errors')

        return parser



class PatchTestInput(PatchTestArgs, PatchTestStdIn):
    """ PatchTest wrapper input class"""
    pass
