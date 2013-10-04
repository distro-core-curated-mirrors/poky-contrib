python multilib_virtclass_handler () {
<<<<<<< HEAD
=======
    if not isinstance(e, bb.event.RecipePreFinalise):
        return

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    cls = e.data.getVar("BBEXTENDCURR", True)
    variant = e.data.getVar("BBEXTENDVARIANT", True)
    if cls != "multilib" or not variant:
        return

    e.data.setVar('STAGING_KERNEL_DIR', e.data.getVar('STAGING_KERNEL_DIR', True))

    # There should only be one kernel in multilib configs
<<<<<<< HEAD
    # We also skip multilib setup for module packages.
    provides = (e.data.getVar("PROVIDES", True) or "").split()
    if "virtual/kernel" in provides or bb.data.inherits_class('module-base', e.data):
        raise bb.parse.SkipPackage("We shouldn't have multilib variants for the kernel")

    save_var_name=e.data.getVar("MULTILIB_SAVE_VARNAME", True) or ""
    for name in save_var_name.split():
        val=e.data.getVar(name, True)
        if val:
            e.data.setVar(name + "_MULTILIB_ORIGINAL", val)

=======
    if bb.data.inherits_class('kernel', e.data) or bb.data.inherits_class('module-base', e.data):
        raise bb.parse.SkipPackage("We shouldn't have multilib variants for the kernel")

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    if bb.data.inherits_class('image', e.data):
        e.data.setVar("MLPREFIX", variant + "-")
        e.data.setVar("PN", variant + "-" + e.data.getVar("PN", False))
        return

<<<<<<< HEAD
    if bb.data.inherits_class('cross-canadian', e.data):
        e.data.setVar("MLPREFIX", variant + "-")
        override = ":virtclass-multilib-" + variant
        e.data.setVar("OVERRIDES", e.data.getVar("OVERRIDES", False) + override)
        bb.data.update_data(e.data)
        return

    if bb.data.inherits_class('native', e.data):
        raise bb.parse.SkipPackage("We can't extend native recipes")

    if bb.data.inherits_class('nativesdk', e.data) or bb.data.inherits_class('crosssdk', e.data):
        raise bb.parse.SkipPackage("We can't extend nativesdk recipes")

    if bb.data.inherits_class('allarch', e.data) and not bb.data.inherits_class('packagegroup', e.data):
        raise bb.parse.SkipPackage("Don't extend allarch recipes which are not packagegroups")

=======
    if bb.data.inherits_class('native', e.data):
        raise bb.parse.SkipPackage("We can't extend native recipes")

    if bb.data.inherits_class('nativesdk', e.data):
        raise bb.parse.SkipPackage("We can't extend nativesdk recipes")

    save_var_name=e.data.getVar("MULTILIB_SAVE_VARNAME", True) or ""
    for name in save_var_name.split():
        val=e.data.getVar(name, True)
        if val:
            e.data.setVar(name + "_MULTILIB_ORIGINAL", val)
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

    # Expand this since this won't work correctly once we set a multilib into place
    e.data.setVar("ALL_MULTILIB_PACKAGE_ARCHS", e.data.getVar("ALL_MULTILIB_PACKAGE_ARCHS", True))
 
    override = ":virtclass-multilib-" + variant

    e.data.setVar("MLPREFIX", variant + "-")
    e.data.setVar("PN", variant + "-" + e.data.getVar("PN", False))
<<<<<<< HEAD
    e.data.setVar("OVERRIDES", e.data.getVar("OVERRIDES", False) + override)

    # Expand the WHITELISTs with multilib prefix
    for whitelist in ["HOSTTOOLS_WHITELIST_GPLv3", "WHITELIST_GPLv3", "LGPLv2_WHITELIST_GPLv3"]:
        pkgs = e.data.getVar(whitelist, True)
        for pkg in pkgs.split():
            pkgs += " " + variant + "-" + pkg
        e.data.setVar(whitelist, pkgs)

    # DEFAULTTUNE can change TARGET_ARCH override so expand this now before update_data
    newtune = e.data.getVar("DEFAULTTUNE_" + "virtclass-multilib-" + variant, False)
    if newtune:
        e.data.setVar("DEFAULTTUNE", newtune)
}

addhandler multilib_virtclass_handler
multilib_virtclass_handler[eventmask] = "bb.event.RecipePreFinalise"
=======
    e.data.setVar("SHLIBSDIR_virtclass-multilib-" + variant ,e.data.getVar("SHLIBSDIR", False) + "/" + variant)
    e.data.setVar("OVERRIDES", e.data.getVar("OVERRIDES", False) + override)
}

addhandler multilib_virtclass_handler
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

STAGINGCC_prepend = "${BBEXTENDVARIANT}-"

python __anonymous () {
    variant = d.getVar("BBEXTENDVARIANT", True)

    import oe.classextend

    clsextend = oe.classextend.ClassExtender(variant, d)

    if bb.data.inherits_class('image', d):
        clsextend.map_depends_variable("PACKAGE_INSTALL")
        clsextend.map_depends_variable("LINGUAS_INSTALL")
        clsextend.map_depends_variable("RDEPENDS")
        pinstall = d.getVar("LINGUAS_INSTALL", True) + " " + d.getVar("PACKAGE_INSTALL", True)
        d.setVar("PACKAGE_INSTALL", pinstall)
        d.setVar("LINGUAS_INSTALL", "")
        # FIXME, we need to map this to something, not delete it!
        d.setVar("PACKAGE_INSTALL_ATTEMPTONLY", "")

    if bb.data.inherits_class('populate_sdk_base', d):
        clsextend.map_depends_variable("TOOLCHAIN_TARGET_TASK")
        clsextend.map_depends_variable("TOOLCHAIN_TARGET_TASK_ATTEMPTONLY")

<<<<<<< HEAD
    if bb.data.inherits_class('image', d):
        return

    clsextend.map_depends_variable("DEPENDS")
    clsextend.map_variable("PROVIDES")

    if bb.data.inherits_class('cross-canadian', d):
=======
    if bb.data.inherits_class('image', d) or bb.data.inherits_class('populate_sdk_base', d):
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        return

    clsextend.rename_packages()
    clsextend.rename_package_variables((d.getVar("PACKAGEVARS", True) or "").split())

<<<<<<< HEAD
    clsextend.map_packagevars()
    clsextend.map_regexp_variable("PACKAGES_DYNAMIC")
    clsextend.map_variable("PACKAGE_INSTALL")
    clsextend.map_variable("INITSCRIPT_PACKAGES")
    clsextend.map_variable("USERADD_PACKAGES")
}

PACKAGEFUNCS_append = " do_package_qa_multilib"
=======
    clsextend.map_depends_variable("DEPENDS")
    clsextend.map_packagevars()
    clsextend.map_variable("PROVIDES")
    clsextend.map_regexp_variable("PACKAGES_DYNAMIC")
    clsextend.map_variable("PACKAGE_INSTALL")
    clsextend.map_variable("INITSCRIPT_PACKAGES")
}

PACKAGEFUNCS_append = "do_package_qa_multilib"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

python do_package_qa_multilib() {

    def check_mlprefix(pkg, var, mlprefix):
        values = bb.utils.explode_deps(d.getVar('%s_%s' % (var, pkg), True) or d.getVar(var, True) or "")
        candidates = []
        for i in values:
            if i.startswith('virtual/'):
                i = i[len('virtual/'):]
<<<<<<< HEAD
            if (not i.startswith('kernel-module')) and (not i.startswith(mlprefix)) and \
                (not 'cross-canadian' in i) and (not i.startswith("nativesdk-")) and \
                (not i.startswith("rtld")):
=======
            if (not i.startswith('kernel-module')) and (not i.startswith(mlprefix)):
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
                candidates.append(i)
        if len(candidates) > 0:
            bb.warn("Multilib QA Issue: %s package %s - suspicious values '%s' in %s" 
                   % (d.getVar('PN', True), pkg, ' '.join(candidates), var))

    ml = d.getVar('MLPREFIX', True)
    if not ml:
        return

    packages = d.getVar('PACKAGES', True)
    for pkg in packages.split():
        check_mlprefix(pkg, 'RDEPENDS', ml)
        check_mlprefix(pkg, 'RPROVIDES', ml)
        check_mlprefix(pkg, 'RRECOMMENDS', ml)
        check_mlprefix(pkg, 'RSUGGESTS', ml)
        check_mlprefix(pkg, 'RREPLACES', ml)
        check_mlprefix(pkg, 'RCONFLICTS', ml)
}
<<<<<<< HEAD
=======

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
