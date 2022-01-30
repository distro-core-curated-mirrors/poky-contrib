#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: GPL-2.0-only
#
# Additional packagedata utilities
#
# Borrowing largely from oe-pkgdata-util
#
# Copyright 2012-2020 Intel Corporation
#

import codecs
import os
import json
import bb.compress.zstd
import oe.path

from glob import glob


class PathNotFoundError(bb.BBHandledException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "Error: %s not found." % self.path

def packaged(pkg, d):
    return os.access(get_subpkgedata_fn(pkg, d) + '.packaged', os.R_OK)

def read_pkgdatafile(fn):
    pkgdata = {}

    def decode(str):
        c = codecs.getdecoder("unicode_escape")
        return c(str)[0]

    if os.access(fn, os.R_OK):
        import re
        with open(fn, 'r') as f:
            lines = f.readlines()
        r = re.compile(r"(^.+?):\s+(.*)")
        for l in lines:
            m = r.match(l)
            if m:
                pkgdata[m.group(1)] = decode(m.group(2))

    return pkgdata

def get_subpkgedata_fn(pkg, d):
    return d.expand('${PKGDATA_DIR}/runtime/%s' % pkg)

def has_subpkgdata(pkg, d):
    return os.access(get_subpkgedata_fn(pkg, d), os.R_OK)

def read_subpkgdata(pkg, d):
    return read_pkgdatafile(get_subpkgedata_fn(pkg, d))

def has_pkgdata(pn, d):
    fn = d.expand('${PKGDATA_DIR}/%s' % pn)
    return os.access(fn, os.R_OK)

def read_pkgdata(pn, d):
    fn = d.expand('${PKGDATA_DIR}/%s' % pn)
    return read_pkgdatafile(fn)

#
# Collapse FOO:pkg variables into FOO
#
def read_subpkgdata_dict(pkg, d):
    ret = {}
    subd = read_pkgdatafile(get_subpkgedata_fn(pkg, d))
    for var in subd:
        newvar = var.replace(":" + pkg, "")
        if newvar == var and var + ":" + pkg in subd:
            continue
        ret[newvar] = subd[var]
    return ret

def read_subpkgdata_extended(pkg, d):
    import json
    import bb.compress.zstd

    fn = d.expand("${PKGDATA_DIR}/extended/%s.json.zstd" % pkg)
    try:
        num_threads = int(d.getVar("BB_NUMBER_THREADS"))
        with bb.compress.zstd.open(fn, "rt", encoding="utf-8", num_threads=num_threads) as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def _pkgmap(d):
    """Return a dictionary mapping package to recipe name."""

    pkgdatadir = d.getVar("PKGDATA_DIR")

    pkgmap = {}
    try:
        files = os.listdir(pkgdatadir)
    except OSError:
        bb.warn("No files in %s?" % pkgdatadir)
        files = []

    for pn in [f for f in files if not os.path.isdir(os.path.join(pkgdatadir, f))]:
        try:
            pkgdata = read_pkgdatafile(os.path.join(pkgdatadir, pn))
        except OSError:
            continue

        packages = pkgdata.get("PACKAGES") or ""
        for pkg in packages.split():
            pkgmap[pkg] = pn

    return pkgmap

def pkgmap(d):
    """Return a dictionary mapping package to recipe name.
    Cache the mapping in the metadata"""

    pkgmap_data = d.getVar("__pkgmap_data", False)
    if pkgmap_data is None:
        pkgmap_data = _pkgmap(d)
        d.setVar("__pkgmap_data", pkgmap_data)

    return pkgmap_data

def recipename(pkg, d):
    """Return the recipe name for the given binary package name."""

    return pkgmap(d).get(pkg)

def foreach_runtime_provider_pkgdata(d, rdep, include_rdep=False):
    pkgdata_dir = d.getVar("PKGDATA_DIR")
    possibles = set()
    try:
        possibles |= set(os.listdir("%s/runtime-rprovides/%s/" % (pkgdata_dir, rdep)))
    except OSError:
        pass

    if include_rdep:
        possibles.add(rdep)

    for p in sorted(list(possibles)):
        rdep_data = read_subpkgdata(p, d)
        yield p, rdep_data

def get_package_mapping(pkg, basepkg, d, depversions=None):
    import oe.packagedata

    data = oe.packagedata.read_subpkgdata(pkg, d)
    key = "PKG:%s" % pkg

    if key in data:
        if bb.data.inherits_class('allarch', d) and bb.data.inherits_class('packagegroup', d) and pkg != data[key]:
            bb.error("An allarch packagegroup shouldn't depend on packages which are dynamically renamed (%s to %s)" % (pkg, data[key]))
        # Have to avoid undoing the write_extra_pkgs(global_variants...)
        if bb.data.inherits_class('allarch', d) and not d.getVar('MULTILIB_VARIANTS') \
            and data[key] == basepkg:
            return pkg
        if depversions == []:
            # Avoid returning a mapping if the renamed package rprovides its original name
            rprovkey = "RPROVIDES:%s" % pkg
            if rprovkey in data:
                if pkg in bb.utils.explode_dep_versions2(data[rprovkey]):
                    bb.note("%s rprovides %s, not replacing the latter" % (data[key], pkg))
                    return pkg
        # Do map to rewritten package name
        return data[key]

    return pkg

def get_package_additional_metadata(pkg_type, d):
    base_key = "PACKAGE_ADD_METADATA"
    for key in ("%s_%s" % (base_key, pkg_type.upper()), base_key):
        if d.getVar(key, False) is None:
            continue
        d.setVarFlag(key, "type", "list")
        if d.getVarFlag(key, "separator") is None:
            d.setVarFlag(key, "separator", "\\n")
        metadata_fields = [field.strip() for field in oe.data.typed_value(key, d)]
        return "\n".join(metadata_fields).strip()

def runtime_mapping_rename(varname, pkg, d):
    #bb.note("%s before: %s" % (varname, d.getVar(varname)))

    new_depends = {}
    deps = bb.utils.explode_dep_versions2(d.getVar(varname) or "")
    for depend, depversions in deps.items():
        new_depend = get_package_mapping(depend, pkg, d, depversions)
        if depend != new_depend:
            bb.note("package name mapping done: %s -> %s" % (depend, new_depend))
        new_depends[new_depend] = deps[depend]

    d.setVar(varname, bb.utils.join_deps(new_depends, commasep=False))

    #bb.note("%s after: %s" % (varname, d.getVar(varname)))

def emit_pkgdata(pkgfiles, d):
    def process_postinst_on_target(pkg, mlprefix):
        pkgval = d.getVar('PKG:%s' % pkg)
        if pkgval is None:
            pkgval = pkg

        defer_fragment = """
if [ -n "$D" ]; then
    $INTERCEPT_DIR/postinst_intercept delay_to_first_boot %s mlprefix=%s
    exit 0
fi
""" % (pkgval, mlprefix)

        postinst = d.getVar('pkg_postinst:%s' % pkg)
        postinst_ontarget = d.getVar('pkg_postinst_ontarget:%s' % pkg)

        if postinst_ontarget:
            bb.debug(1, 'adding deferred pkg_postinst_ontarget() to pkg_postinst() for %s' % pkg)
            if not postinst:
                postinst = '#!/bin/sh\n'
            postinst += defer_fragment
            postinst += postinst_ontarget
            d.setVar('pkg_postinst:%s' % pkg, postinst)

    def add_set_e_to_scriptlets(pkg):
        for scriptlet_name in ('pkg_preinst', 'pkg_postinst', 'pkg_prerm', 'pkg_postrm'):
            scriptlet = d.getVar('%s:%s' % (scriptlet_name, pkg))
            if scriptlet:
                scriptlet_split = scriptlet.split('\n')
                if scriptlet_split[0].startswith("#!"):
                    scriptlet = scriptlet_split[0] + "\nset -e\n" + "\n".join(scriptlet_split[1:])
                else:
                    scriptlet = "set -e\n" + "\n".join(scriptlet_split[0:])
            d.setVar('%s:%s' % (scriptlet_name, pkg), scriptlet)

    def write_if_exists(f, pkg, var):
        def encode(str):
            import codecs
            c = codecs.getencoder("unicode_escape")
            return c(str)[0].decode("latin1")

        val = d.getVar('%s:%s' % (var, pkg))
        if val:
            f.write('%s:%s: %s\n' % (var, pkg, encode(val)))
            return val
        val = d.getVar('%s' % (var))
        if val:
            f.write('%s: %s\n' % (var, encode(val)))
        return val

    def write_extra_pkgs(variants, pn, packages, pkgdatadir):
        for variant in variants:
            with open("%s/%s-%s" % (pkgdatadir, variant, pn), 'w') as fd:
                fd.write("PACKAGES: %s\n" % ' '.join(
                            map(lambda pkg: '%s-%s' % (variant, pkg), packages.split())))

    def write_extra_runtime_pkgs(variants, packages, pkgdatadir):
        for variant in variants:
            for pkg in packages.split():
                ml_pkg = "%s-%s" % (variant, pkg)
                subdata_file = "%s/runtime/%s" % (pkgdatadir, ml_pkg)
                with open(subdata_file, 'w') as fd:
                    fd.write("PKG:%s: %s" % (ml_pkg, pkg))

    packages = d.getVar('PACKAGES')
    pkgdest = d.getVar('PKGDEST')
    pkgdatadir = d.getVar('PKGDESTWORK')

    data_file = pkgdatadir + d.expand("/${PN}")
    with open(data_file, 'w') as fd:
        fd.write("PACKAGES: %s\n" % packages)

    pkgdebugsource = d.getVar("PKGDEBUGSOURCES") or []

    pn = d.getVar('PN')
    global_variants = (d.getVar('MULTILIB_GLOBAL_VARIANTS') or "").split()
    variants = (d.getVar('MULTILIB_VARIANTS') or "").split()

    if bb.data.inherits_class('kernel', d) or bb.data.inherits_class('module-base', d):
        write_extra_pkgs(variants, pn, packages, pkgdatadir)

    if bb.data.inherits_class('allarch', d) and not variants \
        and not bb.data.inherits_class('packagegroup', d):
        write_extra_pkgs(global_variants, pn, packages, pkgdatadir)

    workdir = d.getVar('WORKDIR')

    for pkg in packages.split():
        pkgval = d.getVar('PKG:%s' % pkg)
        if pkgval is None:
            pkgval = pkg
            d.setVar('PKG:%s' % pkg, pkg)

        extended_data = {
            "files_info": {}
        }

        pkgdestpkg = os.path.join(pkgdest, pkg)
        files = {}
        files_extra = {}
        total_size = 0
        seen = set()
        for f in pkgfiles[pkg]:
            fpath = os.sep + os.path.relpath(f, pkgdestpkg)

            fstat = os.lstat(f)
            files[fpath] = fstat.st_size

            extended_data["files_info"].setdefault(fpath, {})
            extended_data["files_info"][fpath]['size'] = fstat.st_size

            if fstat.st_ino not in seen:
                seen.add(fstat.st_ino)
                total_size += fstat.st_size

            if fpath in pkgdebugsource:
                extended_data["files_info"][fpath]['debugsrc'] = pkgdebugsource[fpath]
                del pkgdebugsource[fpath]

        d.setVar('FILES_INFO:' + pkg , json.dumps(files, sort_keys=True))

        process_postinst_on_target(pkg, d.getVar("MLPREFIX"))
        add_set_e_to_scriptlets(pkg)

        subdata_file = pkgdatadir + "/runtime/%s" % pkg
        with open(subdata_file, 'w') as sf:
            for var in (d.getVar('PKGDATA_VARS') or "").split():
                val = write_if_exists(sf, pkg, var)

            write_if_exists(sf, pkg, 'FILERPROVIDESFLIST')
            for dfile in sorted((d.getVar('FILERPROVIDESFLIST:' + pkg) or "").split()):
                write_if_exists(sf, pkg, 'FILERPROVIDES:' + dfile)

            write_if_exists(sf, pkg, 'FILERDEPENDSFLIST')
            for dfile in sorted((d.getVar('FILERDEPENDSFLIST:' + pkg) or "").split()):
                write_if_exists(sf, pkg, 'FILERDEPENDS:' + dfile)

            sf.write('%s:%s: %d\n' % ('PKGSIZE', pkg, total_size))

        subdata_extended_file = pkgdatadir + "/extended/%s.json.zstd" % pkg
        num_threads = int(d.getVar("BB_NUMBER_THREADS"))
        with bb.compress.zstd.open(subdata_extended_file, "wt", encoding="utf-8", num_threads=num_threads) as f:
            json.dump(extended_data, f, sort_keys=True, separators=(",", ":"))

        # Symlinks needed for rprovides lookup
        rprov = d.getVar('RPROVIDES:%s' % pkg) or d.getVar('RPROVIDES')
        if rprov:
            for p in bb.utils.explode_deps(rprov):
                subdata_sym = pkgdatadir + "/runtime-rprovides/%s/%s" % (p, pkg)
                bb.utils.mkdirhier(os.path.dirname(subdata_sym))
                oe.path.relsymlink(subdata_file, subdata_sym, True)

        allow_empty = d.getVar('ALLOW_EMPTY:%s' % pkg)
        if not allow_empty:
            allow_empty = d.getVar('ALLOW_EMPTY')
        root = "%s/%s" % (pkgdest, pkg)
        os.chdir(root)
        g = glob('*')
        if g or allow_empty == "1":
            # Symlinks needed for reverse lookups (from the final package name)
            subdata_sym = pkgdatadir + "/runtime-reverse/%s" % pkgval
            oe.path.relsymlink(subdata_file, subdata_sym, True)

            packagedfile = pkgdatadir + '/runtime/%s.packaged' % pkg
            open(packagedfile, 'w').close()

    if bb.data.inherits_class('kernel', d) or bb.data.inherits_class('module-base', d):
        write_extra_runtime_pkgs(variants, packages, pkgdatadir)

    if bb.data.inherits_class('allarch', d) and not variants \
        and not bb.data.inherits_class('packagegroup', d):
        write_extra_runtime_pkgs(global_variants, packages, pkgdatadir)

def mapping_rename_hook(d):
    """
    Rewrite variables to account for package renaming in things
    like debian.bbclass or manual PKG variable name changes
    """
    pkg = d.getVar("PKG")
    oe.packagedata.runtime_mapping_rename("RDEPENDS", pkg, d)
    oe.packagedata.runtime_mapping_rename("RRECOMMENDS", pkg, d)
    oe.packagedata.runtime_mapping_rename("RSUGGESTS", pkg, d)

def _filerprovidesmap(d):
    """Return a dictionary mapping FILERPROVIDES to (sub)package name."""

    pkgdatadir = d.getVar("PKGDATA_DIR")

    filerprovidesmap = {}
    try:
        files = os.listdir(os.path.join(pkgdatadir, 'runtime'))
    except OSError:
        bb.warn("No files in %s?" % pkgdatadir)
        files = []

    for pkg in [f for f in files if not os.path.isdir(os.path.join(pkgdatadir, 'runtime', f))]:
        try:
            if pkg.endswith('.packaged'):
                continue
            subpkgdata = read_subpkgdata(pkg, d)
            #pkgdata = read_pkgdatafile(os.path.join(pkgdatadir, pkg))
        except OSError:
            continue

        #filerprovides = pkgdata.get("FILERPROVDES") or ""
        bb.debug(1, "subpkgdata: %s" % subpkgdata)
        #filerprovideslist = subpkgdata.get("FILERPROVIDESLIST") or ""
        filerprovideslist = list_pkg_filerprovides(pkg, d)
        bb.debug(1, "fileprovideslist: %s" % filerprovideslist)
        #filerprovides = subpkgdata.get("FILERPROVIDES") or ""
        #bb.debug(1, "fileprovides: %s" % filerprovides)
        for filerprovide in filerprovideslist:
            bb.debug(1, "filerprovide[%s]: %s" % (filerprovide, pkg))
            filerprovidesmap.update({filerprovide: pkg})

    return filerprovidesmap

def filerprovidesmap(d):
    """Return a dictionary mapping FILERPROVIDES to package name.
    Cache the mapping in the metadata"""

    filerprovidesmap_data = d.getVar("__filerprovidesmap_data", False)
    if filerprovidesmap_data is None:
        filerprovidesmap_data = _filerprovidesmap(d)
        d.setVar("__filerprovidesmap_data", filerprovidesmap_data)

    return filerprovidesmap_data

#
# packagedata utility functions based on scripts/oe-pkgdata-util
#

def lookup_pkglist(pkgs, pkgdata_dir, reverse):
    if reverse:
        mappings = OrderedDict()
        for pkg in pkgs:
            revlink = os.path.join(pkgdata_dir, "runtime-reverse", pkg)
            bb.debug(2, revlink)
            if os.path.exists(revlink):
                mappings[pkg] = os.path.basename(os.readlink(revlink))
    else:
        mappings = defaultdict(list)
        for pkg in pkgs:
            pkgfile = os.path.join(pkgdata_dir, 'runtime', pkg)
            if os.path.exists(pkgfile):
                with open(pkgfile, 'r') as f:
                    for line in f:
                        fields = line.rstip().split(': ')
                        if fields[0] == 'PKG_%s' % pkg:
                            mappings[pkg].append(fields[1])
                            break
    return mappings

def list_pkg_filerprovides(pkg, d):
    import json
    import oe.package

    filerprovides = []
    subpkgdata = read_subpkgdata(pkg, d)
    found = False
    try:
        files_info = json.loads(subpkgdata['FILES_INFO']) or dict()
    except (KeyError, AttributeError):
        files_info = dict()
    bb.debug(3, "[%s] FILES_INFO: %s" % (pkg, files_info))
    for _file in files_info:
        bb.debug(3, "_file: %s" % _file)
        try:
            _filerprovides = subpkgdata.get('FILERPROVIDES:%s:%s' % (oe.package.file_translate(_file), pkg)).split() or list()
        except AttributeError:
            _filerprovides = list()
        except KeyError:
            _filerprovides = list()
        finally:
            bb.debug(3, "FILERPROVIDES:%s:%s: %s" % (pkg, _file, _filerprovides))
        if _filerprovides != list():
            found = True
            filerprovides.extend(_filerprovides)
    if not found:
        bb.debug(2, 'Unable to find FILERPROVIDES entry in %s' % subpkgdata)
    return filerprovides


def list_pkg_files(pkg, d):
    import json

    files = []
    subpkgdata = read_subpkgdata(pkg, d)
    found = False
    for key in subpkgdata:
        bb.debug(4, 'subpkgdata: %s' % key)
        if key.startswith('FILES_INFO'):
            found = True
            val = subpkgdata[key]
            bb.debug(4, 'val: %s' % val)
            dictval = json.loads(subpkgdata[key])
            #bb.debug(2, 'dictval: %s' % dictval)
            for fullpath in sorted(dictval):
                bb.debug(4, '[%s] file: %s' % (pkg, fullpath))
                files.append(fullpath)
    if not found:
        bb.error('Unable to find FILES_INFO entry in %s' % subpkgdata)
    return files

def find_path(targetpath, pkgdata_dir, d):
    import json
    import fnmatch

    found = False
    matching_paths = {}
    for root, dirs, files in os.walk(os.path.join(pkgdata_dir, 'runtime')):
        for fn in files:
            with open(os.path.join(root, fn)) as f:
                for line in f:
                    if line.startswith('FILES_INFO:'):
                        val = line.split(':', 1)[1].strip()
                        dictval = json.loads(val)
                        for fullpath in dictval.keys():
                            if fnmatch.fnmatchcase(fullpath, targetpath):
                                found = True
                                matching_paths.update({'%s' % fn: '%s' % fullpath})
    if found:
        return matching_paths
    else:
        raise PathNotFoundError('Unable to find any package producing path %s' % targetpath)
        return None

def find_file_rprovides(file_rprovides, pkgdata_dir, d):
    import re

    found = False
    matching_pkgs = {}
    filerprovides_map = filerprovidesmap(d)
    bb.debug(1, "filerprovidesmap(d): %s" % filerprovides_map)
    #pkg_map = pkgmap(d)
    #bb.debug(1, "pkgmap(d): %s" % pkg_map)
    exit(1)

    for root, dirs, files in os.walk(os.path.join(pkgdata_dir, 'runtime')):
        for fn in files:
            with open(os.path.join(root, fn)) as f:
                for line in f:
                    if line.startswith('FILERPROVIDES:'):
                        val = line.split(': ', 1)[1].strip()
                        listval = val.split(' ')
                        for filerprovide in listval:
                            for frp in file_rprovides.split(','):
                                if frp.startswith("perl >="):
                                    found = True
                                    matching_pkgs.update({'perl': '%s' % frp})
                                elif frp.startswith("perl(-") or frp.startswith("perl(."):
                                    bb.debug(2, "Skipping dependency we don't know how to handle: %s" % frp)
                                    found = True
                                else:
                                    # ignore versioned dependencies for now
                                    # perl(DBI) >= 1.57
                                    # TODO: compare required version to PKGV
                                    safe_frp = frp.split(' ')[0]
                                    bb.debug(4, "(?P<frp>%s)" % re.escape(frp))
                                    regex = re.compile(r"(?P<frp>%s)" % re.escape(safe_frp))
                                    m = re.search(regex, filerprovide)
                                    if m:
                                        found = True
                                        matching_pkgs.update({'%s' % fn: '%s' % safe_frp})
    if found:
        return matching_pkgs
    else:
        bb.debug(2, "Unable to find any package which FILERPROVIDES %s" % file_rprovides)
        #raise PathNotFoundError('Unable to find any package which FILERPROVIDES %s' % file_rprovides)
        return dict()

def package_info(pkg, d, extra=None):
    import re

    pkgdatafile = get_subpkgedata_fn(pkg, d)

    def parse_pkgdatafile(pkgdatafile):
        vars = ['PKGV', 'PKGE', 'PKGR', 'PN', 'PV', 'PE', 'PR', 'PKGSIZE']
        if extra:
            vars += extra
        with open(pkgdatafile, 'r') as f:
            vals = dict()
            _extra = ''
            for line in f:
                for var in vars:
                    m = re.match(var + '(?:_\S+)?:\s*(.+?)\s*$', line)
                    if m:
                        vals[var] = m.group(1)
            pkg_version = vals['PKGV'] or ''
            recipe = vals['PN'] or ''
            recipe_version = vals['PV'] or ''
            pkg_size = vals['PKGSIZE'] or ''
            if 'PKGE' in vals:
                pkg_version = vals['PKGE'] + ":" + pkg_version
            if 'PKGR' in vals:
                pkg_version = pkg_version + "-" + vals['PKGR']
            if 'PE' in vals:
                recipe_version = vals['PE'] + ":" + recipe_version
            if 'PR' in vals:
                recipe_version = recipe_version + "-" + vals['PR']
            if extra:
                for var in extra:
                    if var in vals:
                        val = re.sub(r'\s+', ' ', vals[var])
                        _extra += ' "%s"' % val
            return pkg, pkg_version, recipe, recipe_version, pkg_size, _extra

    parse_pkgdatafile(pkgdatafile)
    # Handle both multiple arguments and multiple values within an arg (old syntax)
#   packages = []
#   if args.file:
#       with open(args.file, 'r') as f:
#           for line in f:
#               splitline = line.split()
#               if splitline:
#                   packages.append(splitline[0])
#   else:
#       for pkgitem in args.pkg:
#           packages.extend(pkgitem.split())
#       if not packages:
#           logger.error("No packages specified")
#           sys.exit(1)
#
#   for pkg in packages:
#       providepkgpath = os.path.join(args.pkgdata_dir, "runtime-rprovides", pkg)
#       if os.path.exists(providepkgpath):
#           for f in os.listdir(providepkgpath):
#               if f != pkg:
#                   print("%s is in the RPROVIDES of %s:" % (pkg, f))
#               pkgdatafile = os.path.join(args.pkgdata_dir, "runtime", f)
#               parse_pkgdatafile(pkgdatafile)
#           continue
#       pkgdatafile = os.path.join(args.pkgdata_dir, "runtime-reverse", pkg)
#       if not os.path.exists(pkgdatafile):
#           logger.error("Unable to find any built runtime package named %s" % pkg)
#           sys.exit(1)
#       parse_pkgdatafile(pkgdatafile)
