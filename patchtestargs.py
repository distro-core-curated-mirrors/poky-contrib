#!/usr/bin/env python

import os
import argparse

# This module contains a Class (PatchTestArgs) and
# the its purpose is to simply store the command line arguments
# passed to the 'patchtest' script. Test cases can import it
# and use it to figure out the values, like the repo directory
# the current mbox/series being tested. See tests/test_sample.py
# test case for usage examples.

class PatchTestArgs:
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

        parser.add_argument('--no-patch',
                            dest='nopatch',
                            action='store_true',
                            help="Do not patch the mbox or series/revision")

        parser.add_argument('--force-patch',
                            dest='forcepatch',
                            action='store_true',
                            help="Tests are executed if ALL input is patched correctly")

        parser.add_argument('--single-branch',
                            dest='singlebranch',
                            action='store_true',
                            help="Merge all mbox/series into a single branch")

        parser.add_argument('--debug', '-d',
                            action='store_true',
                            help='Enable debug output')

        parser.add_argument('--quiet', '-q',
                            action='store_true',
                            help='Print only errors')

        return parser
