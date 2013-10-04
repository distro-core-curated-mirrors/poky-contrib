# Class for packagegroup (package group) recipes

<<<<<<< HEAD
=======
# packagegroup packages are only used to pull in other packages
# via their dependencies. They are empty.
ALLOW_EMPTY = "1"

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
# By default, only the packagegroup package itself is in PACKAGES.
# -dbg and -dev flavours are handled by the anonfunc below.
# This means that packagegroup recipes used to build multiple packagegroup
# packages have to modify PACKAGES after inheriting packagegroup.bbclass.
PACKAGES = "${PN}"

# By default, packagegroup packages do not depend on a certain architecture.
# Only if dependencies are modified by MACHINE_FEATURES, packages
# need to be set to MACHINE_ARCH after inheriting packagegroup.bbclass
<<<<<<< HEAD
inherit allarch
=======
PACKAGE_ARCH = "all"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

# This automatically adds -dbg and -dev flavours of all PACKAGES
# to the list. Their dependencies (RRECOMMENDS) are handled as usual
# by package_depchains in a following step.
<<<<<<< HEAD
# Also mark all packages as ALLOW_EMPTY
python () {
    packages = d.getVar('PACKAGES', True).split()
    genpackages = []
    for pkg in packages:
        d.setVar("ALLOW_EMPTY_%s" % pkg, "1")
        for postfix in ['-dbg', '-dev', '-ptest']:
            genpackages.append(pkg+postfix)
    if d.getVar('PACKAGEGROUP_DISABLE_COMPLEMENTARY', True) != '1':
        d.setVar('PACKAGES', ' '.join(packages+genpackages))
=======
python () {
    if d.getVar('PACKAGEGROUP_DISABLE_COMPLEMENTARY', True) == '1':
        return

    packages = d.getVar('PACKAGES', True).split()
    genpackages = []
    for pkg in packages:
        for postfix in ['-dbg', '-dev']:
            genpackages.append(pkg+postfix)
    d.setVar('PACKAGES', ' '.join(packages+genpackages))
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
}

# We don't want to look at shared library dependencies for the
# dbg packages
DEPCHAIN_DBGDEFAULTDEPS = "1"

# We only need the packaging tasks - disable the rest
do_fetch[noexec] = "1"
do_unpack[noexec] = "1"
do_patch[noexec] = "1"
do_configure[noexec] = "1"
do_compile[noexec] = "1"
do_install[noexec] = "1"
do_populate_sysroot[noexec] = "1"
<<<<<<< HEAD

python () {
    initman = d.getVar("VIRTUAL-RUNTIME_init_manager", True)
    if initman and initman in ['sysvinit', 'systemd'] and not base_contains('DISTRO_FEATURES', initman, True, False, d):
        bb.fatal("Please ensure that your setting of VIRTUAL-RUNTIME_init_manager (%s) matches the entries enabled in DISTRO_FEATURES" % initman)
}

=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
