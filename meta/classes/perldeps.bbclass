# perldeps uses the perl.req script from rpm
# to make an attempt at perl dependencies
# for a given recipe or subpackage
# Borrowing heavily from oe-pkgdata-util

inherit perlnative

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
    bb.debug(4, 'recipedatafile: %s' % recipedatafile)

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
    vendor_perlarchlibdir = os.path.join(perlarchlibdir, 'vendor_perl')
    ptest_path = os.path.join(d.getVar('PTEST_PATH'))
    bb.debug(2, 'perllibdir: %s' % perllibdir)
    core_path = ('%s/%s.pm' % (perllibdir, perl_mod.replace('::', '/')))
    core_arch_path = ('%s/%s.pm' % (perlarchlibdir, perl_mod.replace('::', '/')))
    vendor_path = ('%s/%s.pm' % (vendor_perllibdir, perl_mod.replace('::', '/')))
    vendor_arch_path = ('%s/%s.pm' % (vendor_perlarchlibdir, perl_mod.replace('::', '/')))
    bb.debug(2, 'mod_path: %s' % core_path)
    search_paths = []
    search_paths.append(core_path)
    search_paths.append(core_arch_path)
    search_paths.append(vendor_path)
    search_paths.append(vendor_arch_path)
    found = False
    try:
        for path in search_paths:
            #target_path = oe.packagedata.find_path(path, pkgdata_dir, d)
            target_path = oe.packagedata.find_path('*/%s.pm' % perl_mod.replace('::', '/'), pkgdata_dir, d)
            if target_path:
                found = True
                bb.debug(2, 'target_path: %s' % target_path)
                return path
        if not found:
            raise PathNotFoundError('%s: not found in pkgdata' % perl_mod)
    except PathNotFoundError as e:
        bb.warn("{0}".format(e))
    return None

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
    mod_regex = re.compile('^perl\((.[^\)]+)\).*$')
    m = mod_regex.match(raw_dep)
    if m:
        if m.group():
            perl_dep = m.group(1)
            bb.debug(2, 'perl_dep: %s' % perl_dep)
            try:
                filepath = perl_mod_to_file(perl_dep, d)
                bb.debug(2, 'filepath: %s' % filepath)
            except Exception as e:
                bb.debug(2, '{0}'.format(e))
                pass
        else:
            bb.debug(2, "Didn't know how to handle %s" % raw_dep)

def is_dep_in_rdeps(pkg, rdep, d):
    rdeps = d.getVar('RDEPENDS_pn-$s' % pkg).split(' ')
    missing = []
    for dep in rdeps:
        if rdep == dep:
            bb.debug(2, "[%s] Runtime dependency %s met" % (pkg, rdep))
            return True
        missing.append(dep)
    if len(missing) > 1:
        bb.warn('Possible missing runtime dependency detected:\nRDEPENDS_pn-%s += "%s"' % (pkg, missing[0]))
    else:
        bb.warn('Possible missing runtime dependency detected, but multiple candidates were found\nRDEPENDS_pn-%s += "%s"' % (pkg, ' '.join(missing.split())))
    return False

python do_perldeps() {
    import glob
    import oe.packagedata
    import os
    import subprocess

    pkgs = packages(d)
    perl_exts = (".pl", ".pm", ".ph", ".t")
    '''perl "${RPMNATIVE_DIR}/perl.req --help" # ${list of perl files to check} '''
    perl_req = os.path.join(d.getVar('STAGING_LIBDIR_NATIVE'),'rpm','perl.req')
    #perl_req = os.path.join(d.getVar('STAGING_BINDIR_NATIVE'),'perl.req')
    bb.debug(4, "perl_req: %s" % perl_req)
    for pkg in pkgs:
        bb.debug(2, 'processing package: %s' % pkg)
        files = oe.packagedata.list_pkg_files(pkg, d)
        perl_files = []
        for file in files:
            bb.debug(4, '\t%s' % file)
            # TODO: also bin/ scripts with perl shebang
            # TODO: any other files we would be missing?
            # TODO: split out any /t files to -ptest
            # TODO: ignore any /xt files
            if file.endswith(perl_exts):
                #target_dir = d.getVar('STAGING_DIR_TARGET')
                target_dir = os.path.join('%s' % d.getVar('D'))
                target_file = os.path.join('%s%s' % (target_dir, file))
                #bb.debug(2, '\ttarget_file: %s' % target_file)
                if os.path.exists(target_file): 
                    perl_files.append(os.path.join(target_file))
                else:
                    bb.warn('target_file does not exist: %s\ncheck the path' % target_file)
        #bb.debug(2, 'target_files[%s]:\n %s' % (pkg, perl_files))

    #sources_list = glob.glob(os.path.join(d.getVar('S'),'/*/*/*.pm'))
    #for source in sources_list:
    #    bb.debug(2, source.decode('utf-8'))
    #sources = ' '.join(sources_list)
        sources = ' \n'.join(perl_files)
        bb.debug(4, 'sources: %s' % sources)
        res = subprocess.check_output(['%s' % perl_req, *perl_files])
        #res = subprocess.check_output(['%s' % perl_req, '-h'])
        raw_deps = res.decode('utf-8').split('\n')
        if not raw_deps or raw_deps == ['']:
            bb.debug(2, 'raw_deps[%s] is empty' % pkg)
        else:
            bb.debug(2, 'raw_deps[%s]:' % pkg)
        for dep in raw_deps:
            bb.debug(2, '\t%s' % dep)
        for dep in raw_deps:
            candidate = guess_perl_provider(dep, d)
}

do_perldeps[depends] += "rpm-native:do_populate_sysroot perl-native:do_populate_sysroot ${BPN}:do_packagedata"

# We need packages_split to know what all our subpackages are
# Since we want per-subpackage RDEPENDS, not global recipe RDEPENDS
# We want this to be a manual task, not required
#addtask perldeps after do_packagedata before do_package_qa
addtask perldeps
