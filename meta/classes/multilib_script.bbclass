#
# Recipe needs to set MULTILIB_SCRIPTS in the form <pkgname>:<scriptname>, e.g.
# MULTILIB_SCRIPTS = "${PN}-dev:${bindir}/file1 ${PN}:${base_bindir}/file2"
# to indicate which script files to process from which packages.
#

inherit update-alternatives

PACKAGE_PREPROCESS_FUNCS =+ "multilibscript_rename"

python multilibscript_rename() {
    # Do nothing if multilib isn't being used
    if not d.getVar("MULTILIB_VARIANTS"):
        return

    import glob, oe.path
    pkgd = d.getVar("PKGD")
    mlprefix = d.getVar("MLPREFIX")

    for entry in (d.getVar("MULTILIB_SCRIPTS") or "").split():
        pkg, pattern = entry.split(":")
        for script in glob.glob(oe.path.join(pkgd, pattern)):
            scriptname = os.path.basename(script)
            # Full name of the renamed script *in the rootfs*
            mlname = os.path.join(os.path.dirname(script), mlprefix + scriptname)
            if script != mlname:
                os.rename(script, mlname)
            # Now these need to be target paths
            script = script.replace(pkgd, "")
            mlname = mlname.replace(pkgd, "")
            d.appendVar("ALTERNATIVE_" + pkg, " " + scriptname)
            d.setVarFlag("ALTERNATIVE_LINK_NAME", scriptname, script)
            d.setVarFlag("ALTERNATIVE_TARGET", scriptname, mlname)
            d.appendVar("FILES_" + pkg, " " + mlname)
}
