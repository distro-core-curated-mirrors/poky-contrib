# Recipe creation tool - create handler for perl modules
#
# Copyright (C) 2019 Intel Corporation
#
# SPDX-License-Identifier: GPL-2.0-only
#

import collections
import email
import imp
import glob
import itertools
import json
import logging
import os
from pathlib import Path
import re
import sys
import subprocess
import yaml
from recipetool.create import RecipeHandler

logger = logging.getLogger('recipetool')

tinfoil = None


def tinfoil_init(instance):
    global tinfoil
    tinfoil = instance


class PerlRecipeHandler(RecipeHandler):
    base_pkgdeps = ['perl-core']
    excluded_pkgdeps = ['perl-dbg']

    bbvar_map = {
        'Name': 'PN',
        'Version': 'PV',
        'Home-page': 'HOMEPAGE',
        'Summary': 'SUMMARY',
        'Description': 'DESCRIPTION',
        'License': 'LICENSE',
        'Requires': 'RDEPENDS_${PN}',
        'Provides': 'RPROVIDES_${PN}',
        'Obsoletes': 'RREPLACES_${PN}',
    }

    cpan_mirror = {
        'https://cpan.metacpan.org/CPAN', '${CPAN_MIRROR)',
    }

    # http://search.cpan.org/perldoc?CPAN::Meta::Spec
    # not mapped:
    #   ssleay          Original SSLeay License
    #   sun             Sun Internet Standards Source License (SISSL)
    #   open_source     Other Open Source Initiative (OSI) approved license
    #   unrestricted    Not an OSI approved license, but not restricted
    #
    #   restricted mapped to Proprietary
    metajson_license_map = {
        'agpl_3': 'AGPL-3.0',
        'apache_1_1': 'Apache-1.1',
        'apache_2_0': 'Apache-2.0',
        'artistic_1': 'Artistic-1.0',
        'artistic_2': 'Artistic-2.0',
        'bsd': 'BSD-3-Clause',
        'freebsd': 'BSD-2-Clause',
        'gfdl_1_2': 'GFDL-1.2',
        'gfdl_1_3': 'GFDL-1.3',
        'gpl_1': 'GPL-1.0',
        'gpl_2': 'GPL-2.0',
        'gpl_3': 'GPL-3.0',
        'lgpl_2_1': 'LGPL-2.1',
        'lgpl_3_0': 'LGPL-3.0',
        'mit': 'MIT',
        'mozilla_1_0': 'MPL-1.0',
        'mozilla_1_1': 'MPL-1.1',
        'openss': 'OpenSSL',
        'perl_5': 'Artistic-1.0 | GPL-1.0+',
        'qpl_1_0': 'QPL-1.0',
        'zlib': 'Zlib',
        'restricted': 'Proprietary',
        'unknown': 'UNKNOWN',
    }

    # http://module-build.sourceforge.net/META-spec-v1.4.html
    #
    # NOTE: This specification is significantly less precise
    #       about license types. Due diligence is required.
    # 
    # not mapped:
    #   open_source     Other Open Source Initiative (OSI) approved license
    #   unrestricted    Not an OSI approved license, but not restricted
    #
    #   restricted mapped to Proprietary
    metayaml_license_map = {
        'apache': 'Apache-2.0',
        'apache_1_1': 'Apache-1.1',
        'artistic': 'Artistic-1.0',
        'artistic_2': 'Artistic-2.0',
        'bsd': 'BSD-2-Clause',
        'gpl': 'GPL-2.0 | GPL-3.0',
        'lgpl': 'LGPL-2.0 | LGPL-2.1 | LGPL-3.0',
        'mozilla': 'MPL-1.0 | MPL-1.1',
        'perl': 'Artistic-1.0 | GPL-1.0+',
        'restricted': 'Proprietary',
    }

    def __init__(self):
        self.use_metajson = False
        self.use_metayaml = False
        self.uses_makemaker = False
        self.is_app = False
        self.module_files = []
        self.test_files = []
        self.deps = set()
        self.deps_ptest = set()
        self.unmet_deps = set()
        self.unmet_deps_ptest = set()
        logger.debug("PerlRecipeHandler.__init__")
        pass

    def process(self, srctree, classes, lines_before, lines_after, handled, extravalues):
        logger.debug("PerlRecipeHandler.process")

        if 'buildsystem' in handled:
            logger.debug("buildsystem in handled")
            return False

        if RecipeHandler.checkfiles(srctree, ['META.json']):
            self.use_metajson = True
            logger.debug("META.json found in source")
            self.parse_metajson(srctree, classes, lines_before, lines_after, handled, extravalues)
            pass
        elif RecipeHandler.checkfiles(srctree, ['META.yml']):
            self.use_metayaml = True
            logger.debug("No META.json found in source. Falling back on META.yml found in source")
            self.parse_metayaml(srctree, handled)
            pass
        elif RecipeHandler.checkfiles(srctree, ['Makefile.PL', 'Makefile.pl']):
            logger.debug("No META.json or META.yml found in source. Falling back on Makefile.pl found in source")
            self.uses_makemaker = True
        elif RecipeHandler.checkfiles(srctree, ['Build.PL', 'Build.pl']):
            logger.debug("No META.json, META.yml or Makefile.pl found in source. Falling back on Build.pl found in source")
            self.uses_makemaker = False
        else:
            logger.debug("No META.json, META.yml, Makefile.pl or Build.pl found in source")
            return

        if self.uses_makemaker:
            classes.append('cpan')
            logger.debug('inherit cpan')
        else:
            classes.append('cpan_build')
            logger.debug('inherit cpan_build')

        if self.enable_ptest(srctree):
            classes.append('ptest-perl')
            logger.debug('inherit ptest-perl')

        for root, dirs, files in os.walk(srctree, topdown=True):
            dirs[:] = [d for d in dirs if d not in set('/t')]
            logger.debug("dirs: {}", dirs)
            files[:] = [f for f in files if f.endswith(tuple(['.pm', '.xs']))]
            logger.debug("files: {}", files)
            for f in [os.path.join(root, file_) for file_ in files]:
                self.module_files.append(f)

        if self.module_files:
            for module_file in self.module_files:
                logger.debug('module_file:')
                deps, unmet_deps = self.scan_perl_dependencies(module_file)
                for dep in deps:
                    self.deps.add(dep)
                for unmet in unmet_deps:
                    self.unmet_deps.add(unmet)
            if self.deps:
                lines_after.append('#')
                lines_after.append('# Runtime dependencies have been detected')
                lines_after.append('# An attempt has been made to map them properly')
                lines_after.append('#')
            if self.unmet_deps:
                lines_after.append('# Unmet dependencies have been detected:')
                for unmet in sorted(self.unmet_deps):
                    lines_after.append('# {}'.format(unmet))
            if self.deps:
                lines_after.append('RDEPENDS_${PN} += " \\')
                for dep in sorted(self.deps):
                    lines_after.append( "    {} \\".format(dep))
                lines_after.append('"')
                lines_after.append('')

        if self.test_files:
            for test_file in self.test_files:
                logger.debug('test_file:')
                deps, unmet_deps = self.scan_perl_dependencies(test_file)
                for dep in deps:
                    if dep not in self.deps:
                        self.deps_ptest.add(dep)
                for unmet in unmet_deps:
                    if unmet not in self.unmet_deps:
                        self.unmet_deps_ptest.add(unmet)
            if self.deps_ptest:
                lines_after.append('#')
                lines_after.append('# ptest dependencies have been detected')
                lines_after.append('# An attempt has been made to map them properly')
                lines_after.append('#')
            if self.unmet_deps_ptest:
                lines_after.append('# Unmet dependencies for ptest have been detected:')
                for unmet in sorted(self.unmet_deps_ptest):
                    lines_after.append('#  {}'.format(unmet))
                lines_after.append('#')
            if self.deps_ptest:
                lines_after.append('RDEPENDS_${PN}-ptest += " \\')
                for dep in sorted(self.deps_ptest):
                    lines_after.append( "    {} \\".format(dep))
                lines_after.append('"')
                lines_after.append('')

        lines_after.append('BBCLASSEXTEND = "native nativesdk"')

        # Done editing the recipe
        handled.append('buildsystem')

    def parse_metajson(self, srctree, classes, lines_before, lines_after, handled, extravalues):
        with open(os.path.join(srctree, "META.json"), 'r') as stream:
            try:
                metajson = json.load(stream)
                try:
                    for build_requires in  metajson["prereqs"]["build"]["requires"]:
                       if "ExtUtils::MakeMaker" in build_requires:
                           self.uses_makemaker = True
                except KeyError as e:
                    for configure_requires in metajson["prereqs"]["configure"]["requires"]:
                        if "ExtUtils::MakeMaker" in configure_requires:
                            self.uses_makemaker = True
                self._handle_license(handled, lines_before, lines_after, metajson['license'], self.metajson_license_map)
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(e)
        return

    def parse_metayaml(self, srctree, handled):
        with open(os.path.join(srctree, "META.yml"), 'r') as stream:
            try:
                metayaml = yaml.safe_load(stream)
                for build_requires in  metayaml["build_requires"]:
                    if "ExtUtils::MakeMaker" in build_requires:
                        self.uses_makemaker = True
                self._handle_license(handled, lines_before, lines_after, metayaml['license'], self.metayaml_license_map)
            except yaml.YAMLError as e:
                logger.error(e)
        return

    def enable_ptest(self, srctree):
        root = os.path.join(srctree, r't')
        test_files = [os.path.join(root, file_) for file_ in os.listdir(root) if file_.endswith('.t')]
        if test_files:
            for test_file in test_files:
                self.test_files.append(test_file)
            return True
        return False

    def _handle_license(self, handled, lines_before, lines_after, licsrc, licmap):
        logger.debug('_handle_license')
        logger.debug('licsrc: %s', licsrc)
        try:
            for license in licsrc:
                logger.debug('license detected: %s', license)
                mapped = licmap.get(license)
                logger.debug('mapped license: %s', mapped)
                if mapped:
                    handled.append('license')
                    # lines_after.append('LICENSE = "{}"'.format(mapped))
                else:
                    logger.debug('Failed to map license "%s"', license)
        except Exception as e:
            logger.error(e)
            pass

    def scan_perl_dependencies(self, paths):
        import bb.providers
        logger.debug('paths: %s', paths)
        deps = set()
        unmapped_deps = set() 
        try:
            dep_output = self.run_command(['scandeps.pl', '-B', paths])
        except (OSError, subprocess.CalledProcessError):
            pass
        else:
            for line in dep_output.splitlines():
                logger.debug('line: {}', line)
                # for when scandeps.pl returns a comment and not a match
                if line.startswith('#') or not '=>' in line:
                    continue
                try:
                    dep, min_version = line.split('=>', 1)
                except ValueError as e:
                    logger.debug('Cannot split line: {}', line)
                    raise
                dep.rstrip()
                core_module_naming, lib_module_naming, app_naming = self.debianize(dep)
                core_module_mapped = tinfoil.get_runtime_providers(core_module_naming)
                lib_module_mapped = tinfoil.get_runtime_providers(lib_module_naming)
                if core_module_mapped:
                    deps.add(core_module_naming)
                elif lib_module_mapped:
                    deps.add(lib_module_naming)
                else:
                    # If it didn't map to core module, assume it is an unmet lib module
                    logger.debug('unmapped dependency: %s', lib_module_naming)
                    unmapped_deps.add(lib_module_naming)

        # TODO: remove deps that are provided by this package
        return deps, unmapped_deps

    def debianize(self, perl_name):
        perl_name = perl_name.lower()
        perl_name = perl_name.rstrip()
        perl_name = perl_name.replace("_",'-')
        perl_name = perl_name.replace("::",'-')
        perl_name = perl_name.replace("'", '')
        try:
            core_module_naming = "perl-module-{}".format(perl_name)
            lib_module_naming = "lib{}-perl".format(perl_name)
            app_naming = perl_name
            return core_module_naming, lib_module_naming, app_naming
        except Exception as e:
            logger.error(e)
            raise

    @classmethod
    def run_command(cls, cmd, **popenargs):
        if 'stderr' not in popenargs:
            popenargs['stderr'] = subprocess.STDOUT
        try:
            return subprocess.check_output(cmd, **popenargs).decode('utf-8')
        except OSError as exc:
            logger.error('Unable to run `{}`: {}', ' '.join(cmd), exc)
            raise
        except subprocess.CalledProcessError as exc:
            logger.error('Unable to run `{}`: {}', ' '.join(cmd), exc.output)
            raise

def register_recipe_handlers(handlers):
    # We need to make sure this is ahead of the makefile fallback handler
    handlers.append((PerlRecipeHandler(), 80))
