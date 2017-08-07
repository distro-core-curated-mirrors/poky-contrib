PACKAGE_WRITE_DEPS += "attr-native"
inherit qemu

XATTR_PACKAGES ??= "${PN}"

xattr_settings_common() {
if [ "x$D" != "x" ]; then
    $INTERCEPT_DIR/postinst_intercept setfattr -n user.name -v test ${bindir}/curl
else
    ${bindir}/setfattr -n user.name -v test ${bindir}/curl
fi
}

python populate_packages_append () {
    packages = d.getVar('XATTR_PACKAGES').split()

    for pkg in packages:
        bb.note("adding xattr postinst script to %s" % pkg)

        postinst = d.getVar('pkg_postinst_%s' % pkg)
        if not postinst:
            postinst = '#!/bin/sh\n'
        postinst += d.getVar('xattr_settings_common')
        d.setVar('pkg_postinst_%s' % pkg, postinst)

}

