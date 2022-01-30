# perldeps uses the perl.req script from rpm
# to make an attempt at perl dependencies
# for a given recipe or subpackage
# Borrowing heavily from oe-pkgdata-util

inherit perlnative perl-version

def packages(d):
    import os

    # import subprocess
    # import oe.packagedata

    # wishful thinking, times out because it cannot connect to bitbake
    # pkgs = subprocess.check_output(['oe-pkgdata-util', 'list-pkgs', '-p', d.getVar('BPN')])
    # for pkg in pkgs:
    #    bb.debug(2, pkg)
    #
    # at least for perl, this is not including the subpackages
    # for pkg in d.getVar('PACKAGES').split():
    #    bb.debug(2, pkg)
    # return d.getVar('PACKAGES')
    pkgdata_dir = d.getVar('PKGDATA_DIR')
    bb.debug(2, 'PKGDATA_DIR: %s' % pkgdata_dir)

    recipe = d.getVar('PN')
    bb.debug(2, 'recipe: %s' % recipe)

    recipedatafile = os.path.join(pkgdata_dir, recipe)
    bb.debug(3, 'recipedatafile: %s' % recipedatafile)

    packages = []
    with open(recipedatafile, 'r') as f:
        for line in f:
            fields = line.rstrip().split(': ')
            if fields[0] == 'PACKAGES':
                packages = fields[1].split()
                break

    pkglist = []
    for pkg in packages:
        if os.path.exists(os.path.join(pkgdata_dir, 'runtime', '%s.packaged' % pkg)):
            pkglist.append(pkg)
            bb.debug(2, 'pkglist.append: %s' % pkg)
    return pkglist

def perl_mod_to_file(perl_mod, d):
    import oe.packagedata
    from oe.packagedata import PathNotFoundError

    pkgdata_dir = d.getVar('PKGDATA_DIR')
    perllibdir = os.path.join(d.getVar('libdir'), d.getVar('PERL_OWN_DIR'), 'perl5', get_perl_version(d))
    perlarchlibdir = os.path.join(perllibdir, get_perl_arch(d))
    vendor_perllibdir = os.path.join(d.getVar('libdir'), d.getVar('PERL_OWN_DIR'), 'perl5', 'vendor_perl', get_perl_version(d))
    vendor_perlarchlibdir = os.path.join(vendor_perllibdir, get_perl_arch(d))
    ptestdir = os.path.join(d.getVar('PTEST_PATH'))
    bb.debug(2, 'perllibdir: %s' % perllibdir)
    core_path = ('%s/%s.pm' % (perllibdir, perl_mod.replace('::', '/')))
    core_arch_path = ('%s/%s.pm' % (perlarchlibdir, perl_mod.replace('::', '/')))
    vendor_path = ('%s/%s.pm' % (vendor_perllibdir, perl_mod.replace('::', '/')))
    vendor_arch_path = ('%s/%s.pm' % (vendor_perlarchlibdir, perl_mod.replace('::', '/')))
    ptest_path = ('%s/%s.pm' % (ptestdir, perl_mod.replace('::', '/')))
    bb.debug(2, 'mod_path: %s' % core_path)
    search_paths = []
    search_paths.append(core_path)
    search_paths.append(core_arch_path)
    search_paths.append(vendor_path)
    search_paths.append(vendor_arch_path)
    search_paths.append(ptest_path)
    found = False
    target_path_dict = None
    for path in search_paths:
        try:
            bb.debug(2, "Searching for path: %s in pkgdata" % path)
            target_path_dict = oe.packagedata.find_path(path, pkgdata_dir, d)
            #target_path = oe.packagedata.find_path('*/%s.pm' % perl_mod.replace('::', '/'), pkgdata_dir, d)
        except Exception as e:
            #bb.debug(2, "{0}".format(e))
            pass
        if target_path_dict:
            found = True
            provider, target_path = next(iter(target_path_dict.items()))
            bb.debug(2, 'Resolved path: %s is provided by package: %s' % (target_path, provider))
            if len(target_path_dict) > 1:
                bb.debug(2, "Found more than one provider for perl_mod: %s" % perl_mod)
            return path, provider
    if not found:
       raise PathNotFoundError('%s: not found in pkgdata' % perl_mod)
       return None, None

def guess_perl_provider(raw_dep, d):

    import re

    # deps look like:
    # perl >= 0:5.000
    # (we use a regex to ignore this)
    #
    # perl(My::Awesome::Module)
    # or
    # perl(My::Versioned::Module) >= 1.000
    # TODO: check for sufficient version
    #
    # FIXME: perl >= 0:5.005003
    # /^(?'perl'perl)?((?>\()(?'module'.[^\(\)]+)(?=\)))?|(?= >= )?(?'epoch'\d[[^:])|(?'version'[\d\.]+)$/gm
    #mod_regex = re.compile('^perl\((.[^\):]+)\).*$')
    mod_regex = re.compile("^(?P<perl>perl)?(\((?P<module>.[^\(\)]+)(?=\)))?|(?= >= )?(?P<epoch>\d[[^:])|(?P<version>[\d\.]+)$")
    m = mod_regex.match(raw_dep)
    if m:
        if m.group():
            bb.debug(2, 'm.group(): %s' % m.group())
            if m.group('module'):
                bb.debug(2, 'module_dep: %s' % m.group('module'))
                perl_dep = m.group('module')
            elif m.group('perl'):
                return 'perl'
            bb.debug(2, 'raw_dep: %s' % raw_dep)
            bb.debug(2, 'perl_dep: %s' % perl_dep)
            try:
                filepath, provider = perl_mod_to_file(perl_dep, d)
                bb.debug(2, 'filepath: %s' % filepath)
                bb.debug(2, 'provider: %s' % provider)
                bb.debug(2, "----------------------------")
                return provider
            except Exception as e:
                bb.debug(2, '{0}'.format(e))
                pass
        else:
            bb.debug(2, "Didn't know how to handle %s" % raw_dep)
    return None

def is_dep_in_rdeps(pkg, rdep, d):
    # TODO: check first if rdep is provided by perl itself
    if pkg == rdep:
        return True
    rdeps = []
    try:
        pkgdata_dict = oe.packagedata.read_subpkgdata_dict(pkg, d)
        #bb.debug(2, "%s" % pkgdata_dict.keys())
        #rdeps = [ item.strip() for item in (d.getVar('RDEPENDS:' + pkg)).split() ]
        #rdeps = [ item.strip() for item in (pkgdata_dict['RDEPENDS']).split() ]
        rdeps = bb.utils.explode_deps(pkgdata_dict['RDEPENDS'])
        bb.debug(3, "len(rdeps) = %s" % len(rdeps))
        bb.debug(2, "RDEPENDS:%s: %s" % (pkg, ' '.join(rdeps)))
    except AttributeError:
        bb.debug(2, "RDEPENDS:%s is empty" % pkg)
        return None
    except KeyError:
        bb.debug(2, "RDEPENDS:%s is not defined in pkgdata" % pkg)
        return None
    missing = []
    if rdep in rdeps:
        bb.debug(2, "[%s] Runtime dependency %s met" % (pkg, rdep))
        return True
    elif rdep.startswith("perl-module-") and ("perl-modules" in rdeps):
        bb.debug(2, "[%s] Runtime dependency %s met by perl-modules" % (pkg, rdep))
        return True
    else:
        bb.debug(2, "[%s] Runtime dependency %s NOT met" % (pkg, rdep))
        missing.append(rdep)
    if len(missing) == 0:
        bb.warn("We should not have gotten here: len(missing) == 0")
        return True
    elif len(missing) > 1:
        bb.debug(2, 'Possible missing runtime dependency detected, but multiple candidates were found\nRDEPENDS:%s += "%s"' % (pkg, ' '.join(missing)))
    else:
        bb.debug(2, 'Possible missing runtime dependency detected:\nRDEPENDS:%s += "%s"' % (pkg, missing[0]))
    return False

python do_perldeps() {
    import glob
    import oe.packagedata
    import os
    import subprocess

    pkgs = packages(d)
    # FIXME:
    # needs to be split up for packages-split
    # missing_rdeps[pkg] = set()
    # unresolved_rdeps[pkg] = set()
    # tmp/work/core2-64-poky-linux/libdbd-sqlite-perl/1.66-r0/packages-split/libdbd-sqlite-perl-ptest/usr/lib/libdbd-sqlite-perl/ptest/t/lib
    missing_rdeps = dict()
    unresolved_rdeps = dict()
    perl_exts = (".pl", ".pm", ".ph", ".t")
    '''perl "${RPMNATIVE_DIR}/perl.req --help" # ${list of perl files to check} '''
    perl_req = os.path.join(d.getVar('STAGING_LIBDIR_NATIVE'),'rpm','perl.req')
    #perl_req = os.path.join(d.getVar('STAGING_BINDIR_NATIVE'),'perl.req')
    bb.debug(3, "perl_req: %s" % perl_req)
    for pkg in pkgs:
        missing_rdeps[pkg] = set()
        unresolved_rdeps[pkg] = set()
        if pkg.endswith(('-dbg', '-dev', '-doc', '-src', '-staticdev')):
            continue
        bb.debug(2, '--------------------')
        bb.debug(2, 'processing package: %s' % pkg)
        files = oe.packagedata.list_pkg_files(pkg, d)
        perl_files = []
        for file in files:
            bb.debug(3, '\t%s' % file)
            # TODO: also bin/ scripts with perl shebang
            # TODO: any other files we would be missing?
            # TODO: split out any /t files to -ptest
            # TODO: ignore any /xt files
            if file.endswith(perl_exts):
                #target_dir = d.getVar('STAGING_DIR_TARGET')
                #target_dir = os.path.join('%s/%s' % (d.getVar('PKGDEST'), pkg))
                #target_dir = os.path.join('%s/%s' % (d.getVar('WORKDIR'),'sysroot-destdir'))
                #target_dir = os.path.join('%s' % (d.getVar('D')))
                # NOTE: if the recipes mucks with e.g. do_install_ptest, packages-split will not
                #       exist. libdbd-sqlite-perl is such an offender
                target_dir = os.path.join('%s/%s/%s' % (d.getVar('WORKDIR'), 'packages-split', pkg))
                target_file = os.path.join('%s%s' % (target_dir, file))
                #bb.debug(2, '\ttarget_file: %s' % target_file)
                if not os.path.exists(target_dir):
                    bb.warn('${WORKDIR}/packages-split/%s does not exist:\n\t\tthis task assumes you have built the package from scratch (not sstate)' % pkg)
                if os.path.exists(target_file):
                    perl_files.append(os.path.join(target_file))
                else:
                    bb.warn('${WORKDIR}/packages-split/%s/%s does not exist:\n\t\tthis task assumes you have built the package from scratch (not sstate)' % (pkg,file))
        #bb.debug(2, 'target_files[%s]:\n %s' % (pkg, perl_files))

    #sources_list = glob.glob(os.path.join(d.getVar('S'),'/*/*/*.pm'))
    #for source in sources_list:
    #    bb.debug(2, source.decode('utf-8'))
    #sources = ' '.join(sources_list)
        sources = ' \n'.join(perl_files)
        bb.debug(3, 'sources: %s' % sources)
        res = subprocess.check_output(['%s' % perl_req, *perl_files])
        #res = subprocess.check_output(['%s' % perl_req, '-h'])
        # NOTE: perl.req is not exhuastive, run-time testing is still
        #       required to make certain that all dependencies from all
        #       code paths have been met
        raw_deps = list(filter(None, res.decode('utf-8').split('\n')))
        if not raw_deps or raw_deps == [''] or raw_deps == [' ']:
            bb.debug(2, 'raw_deps[%s] is empty' % pkg)
            continue
        else:
            bb.debug(2, 'raw_deps[%s]:' % pkg)
        for dep in raw_deps:
            bb.debug(2, '\t%s' % dep)
        for dep in raw_deps:
            bb.debug(2, 'processing raw_dep: %s' % dep)
            pkgdata_dir = d.getVar('PKGDATA_DIR')
            providers_dict = oe.packagedata.find_file_rprovides(dep, pkgdata_dir, d)
            bb.debug(2, "providers_dict: %s" % providers_dict)
            for key, value in providers_dict.items():
                if dep in value:
                    if is_dep_in_rdeps(pkg, key, d):
                        bb.debug(2, "Dependency %s met by %s" % (dep, key))
                        continue
                    else:
                        bb.debug(2, "%s has a runtime dependency on %s, but it is not in RDEPENDS" % (pkg, key))
                        missing_rdeps[pkg].add(key)
                else:
                    bb.debug(2, "Dependency %s not resolved in FILERPROVIDES from pkgdata" % dep)
                    unresolved_rdeps[pkg].add(dep)
#           candidate = guess_perl_provider(dep, d)
#           bb.debug(2, "candidate: %s" % candidate)
#           if candidate:
#               if candidate == "perl":
#                   bb.debug(2, "Dependency %s met by perl itself" % dep)
#               if is_dep_in_rdeps(pkg, candidate, d):
#                   bb.debug(2, "Dependency %s met" % candidate)
#               if is_dep_in_rdeps(pkg, dep, d) is False: # exclude None
#                   bb.warn("%s has a runtime dependency on %s, but it is not in RDEPENDS" % (pkg, candidate))
#                   missing_rdeps[pkg].add(candidate)
#           else:
#               bb.warn("%s has a runtime dependency on %s, but it could not be resolved" % (pkg, dep))
#               unresolved_rdeps[pkg].add(dep)
        bb.debug(3, 'len(unresolved_rdeps[%s]) = %s' % (pkg, len(unresolved_rdeps[pkg])))
        if len(unresolved_rdeps[pkg]) != 0:
            bb.debug(2, 'unresolved_rdeps[%s]:' % pkg)
            for udep in unresolved_rdeps[pkg]:
                bb.debug(2, '\t%s' % udep)
        if len(unresolved_rdeps[pkg]) == 0:
            bb.debug(2, "%s seems to have all runtime dependencies resolved" % pkg)
        elif len(unresolved_rdeps[pkg]) > 1:
            bb.warn('[%s] Possible missing runtime dependencies detected, but they could not be resolved "%s"' % (pkg, ' '.join(unresolved_rdeps[pkg])))
        else:
            bb.warn('[%s] Possible missing runtime dependency detected, but it could not be resolved "%s"' % (pkg, unresolved_rdeps[pkg]))
        bb.debug(3, 'len(missing_rdeps[%s]) = %s' % (pkg, len(missing_rdeps[pkg])))
        if len(missing_rdeps[pkg]) == 0:
            bb.debug(2, "%s seems to have all runtime dependencies met" % pkg)
        elif len(missing_rdeps[pkg]) > 1:
            bb.warn('Possible missing runtime dependencies detected\nRDEPENDS:%s += "%s"' % (pkg, ' '.join(missing_rdeps[pkg])))
        else:
            bb.warn('Possible missing runtime dependency detected:\nRDEPENDS:%s += "%s"' % (pkg, missing_rdeps[pkg]))
}

do_perldeps[depends] += "rpm-native:do_populate_sysroot perl-native:do_populate_sysroot ${BPN}:do_packagedata"
do_perldeps[nostamp] = "1"

# We need packages_split to know what all our subpackages are
# Since we want per-subpackage RDEPENDS, not global recipe RDEPENDS
# We want this to be a manual task, not required
#addtask perldeps after do_packagedata before do_package_qa
addtask perldeps
