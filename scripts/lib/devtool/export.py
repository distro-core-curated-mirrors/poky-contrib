# Development tool - export command plugin
#
# Copyright (C) 2014-2017 Intel Corporation
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
"""Devtool export plugin"""

import os
import argparse
import tarfile
import logging

logger = logging.getLogger('devtool')
default_arcname = "workspace.tar"

def export(args, config, basepath, workspace):
    """Entry point for the devtool 'export' subcommand"""

    def create_arcname(name):
        """Create arc name by removing the workspace path or $HOME prefix from name"""
        _name = name
        if name.startswith(config.workspace_path):
            _name = name.replace(config.workspace_path, '')
        else:
            _name = name.replace(os.environ['HOME'], '')
        return (name, _name)

    def reset(tarinfo):
        tarinfo.uname = tarinfo.gname = "nobody"
        return tarinfo

    def add(tar, value):
        # Get  arcnames
        arcnames = []
        for key in ['srctree', 'bbappend', 'recipefile']:
            if key in value and value[key]:
                arcnames.append(create_arcname(value[key]))

        # Archive
        for name, arcname in arcnames:
            tar.add(name, arcname=arcname, filter=reset)

    # include the default archiver filename if missing
    name = args.name
    if os.path.isdir(name):
        if name[-1] != '/':
            name = name + '/'
        name = name + default_arcname

    if os.path.exists(name) and not args.force:
        logger.error('Tar archive %s exists. Use -f to force removal')
        return 1

    included = []
    with tarfile.open(name, "w") as tar:
        if args.include:
            for recipe in args.include:
                if recipe in workspace:
                    add(tar, workspace[recipe])
                    included.append(recipe)
                else:
                    logger.warn('recipe %s not in workspace, not in archive file')
        else:
            for recipe, value in workspace.items():
                if recipe not in args.exclude:
                    add(tar, value)
                    included.append(recipe)

    logger.info('Tar archive create at %s with the following recipes: %s' % (name, included))

def register_commands(subparsers, context):
    """Register devtool export subcommands"""
    parser = subparsers.add_parser('export',
                                   help='Export workspace into a tar archive',
                                   description='Export one or more recipes from current workspace into a tar archive',
                                   group='advanced')

    parser.add_argument('--name', '-n', default=default_arcname, help='Name of the tar archive')
    parser.add_argument('--force', '-f', action="store_true", help='Overwrite previous export tar archive')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--include', '-i', nargs='+', default=[], help='Include the defined recipes into the tar archive')
    group.add_argument('--exclude', '-e', nargs='+', default=[], help='Exclude the defined recipes into the tar archive')
    parser.set_defaults(func=export)
