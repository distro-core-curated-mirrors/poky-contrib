# Recipe creation tool - perl CPAN module support plugin
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

import json
import logging
import os
import re
import requests
import shutil
import subprocess
import tempfile
from recipetool.create import RecipeHandler, split_pkg_licenses, handle_license_vars
from recipetool.metacpan.query import AbstractQuery, AuthorQuery, BuildDependsQuery, HomepageQuery, LicenseQuery, PauseIdQuery

logger = logging.getLogger('recipetool')

plugins = None
tinfoil = None

def plugin_init(pluginlist):
    # Take a reference to the list so we can use it later
    global plugins
    plugins = pluginlist

def tinfoil_init(instance):
    global tinfoil
    tinfoil = instance


class CpanRecipeHandler(RecipeHandler):

    def process(self, srctree, classes, lines_before, lines_after, handled, extravalues):
        import bb.utils
        import bb.providers
        import oe
        from collections import OrderedDict

        if 'buildsystem' in handled:
            return False

        def read_meta_json(fn):
            with open(fn, 'r', errors='surrogateescape') as f:
                return json.loads(f.read())

        # FIXME: really old modules will have META.yml and not META.json
        files = RecipeHandler.checkfiles(srctree, ['META.json'])
        logger.debug( bb.providers.getRuntimeProviders(tinfoil.cooker_data, 'libxml-perl'))
        if files:
            data = read_meta_json(files[0])
            if 'name' in data and 'version' in data:
                extravalues['PN'] = "lib%s-perl" % data['name'].lower()
                extravalues['PV'] = data['version']
                logger.debug("PN = \"%s\"" % extravalues['PN'])
                logger.debug("PV = \"%s\"" % extravalues['PV'])
                pq = PauseIdQuery(pn=data['name'], pv=data['version'])
                logger.debug("PauseIdQuery.pauseid = %s" % pq.pauseid)
                aq = AuthorQuery(pauseid=pq.pauseid)
                logger.debug("AuthorQuery.author = %s" % aq.author)
                if aq.author != None:
                    extravalues['AUTHOR'] = aq.author
                    logger.debug("AUTHOR = \"%s\"" % extravalues['AUTHOR'])
                classes.append('cpan')
                handled.append('buildsystem')
                absq = AbstractQuery(pn=data['name'], pv=data['version'])
                if absq.abstract != None:
                    extravalues['SUMMARY'] = absq.abstract
                    logger.debug("SUMMARY = \"%s\"" % extravalues['SUMMARY'])
                hpq = HomepageQuery(pn=data['name'], pv=data['version'])
                if hpq.homepage != None:
                    extravalues['HOMEPAGE'] = hqp.homepage
                    logger.debug("HOMEPAGE = \"%s\"" % extravalues['HOMEPAGE'])
                lq = LicenseQuery(pn=data['name'], pv=data['version'])
                # if no license in response, try looking for LICENSE file and match text
                # otherwise, look in README for typical copyright/license clause
                # finally, punt and leave it to the user
                try:
                    license_file = RecipeHandler.checkfiles(srctree, ['LICENSE'])[0]
                except IndexError:
                    license_file = False
                try:
                    readme_file = RecipeHandler.checkfiles(srctree, ['README'])[0]
                except IndexError:
                    readme_file = False
                if license_file:
                    if "under the same terms as Perl itself." in open(license_file, 'r').read():
                        extravalues['LICENSE'] = "Artistic-1.0 | GPL-1.0+"
                        logger.debug("LICENSE = \"%s\"" % extravalues['LICENSE'])
                    else:
                        # figure out another way to determine the license from the license file
                        extravalues['LICENSE'] = "Unknown"
                        logger.debug("LICENSE = \"%s\"" % extravalues['LICENSE'])
                    perl_license = re.compile(r"This program is free software; you may redistribute it and/or modify it under the same terms as Perl itself.")
                    with open(license_file, 'r') as f:
                        logger.warn("LICENSE: %s" % f.read())
                        logger.warn('re.search %s ' % re.search("under the same terms as Perl itself", f.read()))
                        logger.warn('perl_license.search %s ' % perl_license.search(f.read()))
                        logger.warn('perl_license.match %s ' % perl_license.match(f.read()))
                        if perl_license.match(f.read()):
                            logger.warn('LICENSE file matches perl_5 license')
                            extravalues['LICENSE'] = "Artistic-1.0 | GPL-1.0+"
                if readme_file:
                    # need to match COPYRIGHT text and use beginline endline
                    if "under the same terms as Perl itself." in open(readme_file, 'r').read():
                        # need to handle similar to guess_license in create.py
                        extravalues['LICENSE'] = "Artistic-1.0 | GPL-1.0+"
                        logger.debug("LICENSE = \"%s\"" % extravalues['LICENSE'])
                    else:
                        # figure out another way to determine the license from the readme file
                        extravalues['LICENSE'] = "Unknown"
                        logger.debug("LICENSE = \"%s\"" % extravalues['LICENSE'])
                elif lq.license != None:
                    extravalues['LICENSE'] = lq.license
                    logger.debug("LICENSE = \"%s\"" % extravalues['LICENSE'])
                deps = data.get('dependencies', {})
                logger.warn(deps)
                bdq = BuildDependsQuery(pn=data['name'], pv=data['version'])

                #updated = self._handle_dependencies(tinfoil.config_data, deps, lines_before, srctree)
                #if updated:
                    # We need to redo the license stuff
                #    self._replace_license_vars(srctree, lines_before, handled, extravalues, tinfoil.config_data)
                #    if line.startswith('LICENSE = '):
                #        lines_before[i] = 'LICENSE = "%s"' % ' & '.join(all_licenses)

                # Need to move S setting after inherit npm
                for i, line in enumerate(lines_before):
                    if line.startswith('S ='):
                        lines_before.pop(i)
                        lines_after.insert(0, '# Must be set after inherit npm since that itself sets S')
                        lines_after.insert(1, line)
                        break

                return True

        return False

#    def _handle_dependencies(self, d, deps, lines_before, srctree):
#        import scriptutils
        #declared_build_deps = #_build_dependency_query()
        #declared_runtime_deps = #_runtime_dependency_query()
        #declared_test_deps = #_test_dependency_query()
#        return declared_build_deps

def register_recipe_handlers(handlers):
    handlers.append((CpanRecipeHandler(), 80))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
