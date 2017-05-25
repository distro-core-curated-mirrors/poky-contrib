# Development tool - import command plugin
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
"""Devtool import plugin"""

import os
import tarfile
import logging
import re
from devtool import standard

logger = logging.getLogger('devtool')

def devimport(args, config, basepath, workspace):
    """Entry point for the devtool 'import' subcommand"""
    if not os.path.exists(args.name):
        logger.error('Tar archive %s does not exist. The expected archive should be created with "devtool export"')
        return 1

    # match exported workspace folders
    prog = re.compile('recipes|appends|sources')

    def get_prefix(name):
        """Prefix the workspace path or $HOME to the member name"""
        _prefix = ""
        if prog.match(name):
            _prefix = config.workspace_path + '/'
        else:
            if not name.startswith('/'):
                _prefix = os.environ['HOME'] + '/'

        return _prefix, _prefix + name

    # include the default archiver filename if missing
    name = args.name
    if os.path.isdir(name):
        if name[-1] != '/':
            name = name + '/'
        name = name + default_arcname

    if not os.path.exists(name):
        logger.error('Tar archive %s does not exists. Export your workspace using "devtool export"')
        return 1

    included = []
    with tarfile.open(name) as tar:
        for member in tar.getmembers():
            prefix, path = get_prefix(member.name)
            if os.path.exists(path):
                if args.force:
                    try:
                        tar.extract(member, path=prefix)
                    except PermissionError as pe:
                        logger.warn(pe)
                else:
                    logger.warn('File already present, add -f to overwrite: %s' % member.name)
            else:
                tar.extract(member, path=prefix)

            # md5 creation just for recipes or appends
            if member.name.startswith('recipes') or member.name.startswith('appends'):
                dirpath, recipe = os.path.split(member.name)
                recipename = ""
                for sep in "_ .".split():
                    if sep in recipe:
                        recipename = recipe.split(sep)[0]
                        break
                if not recipename:
                    logger.warn('Recipe name could not be extracted from %s' % member.name)
                    recipename = recipe

                standard._add_md5(config, recipename, path)
                if recipename not in included:
                    included.append(recipename)

    logger.info('Imported recipes into workspace %s: %s' % (config.workspace_path, included))

def register_commands(subparsers, context):
    """Register devtool import subcommands"""
    parser = subparsers.add_parser('import',
                                   help='Import tar archive into workspace',
                                   description='Import previously created tar archive into the workspace',
                                   group='advanced')
    parser.add_argument('--name', '-n', default='workspace.tar', help='Name of the tar archive to import')
    parser.add_argument('--force', '-f', action="store_true", help='Overwrite previous files')
    parser.set_defaults(func=devimport)
