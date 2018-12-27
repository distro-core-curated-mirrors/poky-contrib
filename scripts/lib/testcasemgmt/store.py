# test case management tool - store test result
#
# Copyright (c) 2018, Intel Corporation.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
from testcasemgmt.gitstore import GitStore

def store(args, logger):
    gitstore = GitStore(args.git_dir, args.git_branch)
    gitstore.store_test_result(logger, args.source_dir, args.git_sub_dir, args.overwrite_result)
    return 0

def register_commands(subparsers):
    """Register subcommands from this plugin"""
    parser_build = subparsers.add_parser('store', help='store test result files into git repository',
                                         description='store the testresults.json file from the source directory into '
                                                     'the destination git repository with the given git branch',
                                         group='store')
    parser_build.set_defaults(func=store)
    parser_build.add_argument('source_dir',
                              help='source directory that contain the test result files to be stored')
    parser_build.add_argument('git_branch', help='git branch (new or existing) used to store the test result files')
    parser_build.add_argument('-d', '--git-dir', default='',
                              help='(optional) destination directory (new or existing) to be used as git repository '
                                   'to store the test result files from the source directory where '
                                   'default location for destination directory will be <top_dir>/testresults')
    parser_build.add_argument('-s', '--git-sub-dir', default='',
                              help='(optional) additional sub directory (new or existing) under the destination '
                                   'directory (git-dir) where it will be used to hold the test result files, used '
                                   'this if storing multiple test result files')
    parser_build.add_argument('-o', '--overwrite-result', action='store_true',
                              help='(optional) overwrite existing test result file with new file provided')
