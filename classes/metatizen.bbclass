python () {
    if bb.data.inherits_class('rootfs_rpm', d):
        rootfsdepends = d.getVarFlag("do_rootfs", "depends", True)
        rootfsdepends = rootfsdepends.replace("rpmresolve-native:do_populate_sysroot", "")
        d.setVarFlag("do_rootfs", "depends", rootfsdepends)
    if bb.data.inherits_class('image-live', d):
        bootimgdepends = d.getVarFlag("do_bootimg", "depends", True)
        bootimgdepends = bootimgdepends.replace(d.expand("${INITRD_IMAGE}:do_rootfs"), "")
        d.setVarFlag("do_bootimg", "depends", bootimgdepends)
}

RPM_EXTRA_PKGDATA = "1"

def package_rpm_extra_pkgdata(splitname, spec_file, d):
    if localdata.getVar('MANIFESTFILES', True):
        spec_file.append('%%manifest %s' %  localdata.getVar('MANIFESTFILES', True))

