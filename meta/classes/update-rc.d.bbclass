UPDATERCPN ?= "${PN}"

DEPENDS_append = " update-rc.d-native"
UPDATERCD = "update-rc.d"
UPDATERCD_virtclass-cross = ""
<<<<<<< HEAD
UPDATERCD_class-native = ""
UPDATERCD_class-nativesdk = ""

RRECOMMENDS_${UPDATERCPN}_append = " ${UPDATERCD}"
=======
UPDATERCD_virtclass-native = ""
UPDATERCD_virtclass-nativesdk = ""

RDEPENDS_${UPDATERCPN}_append = " ${UPDATERCD}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

INITSCRIPT_PARAMS ?= "defaults"

INIT_D_DIR = "${sysconfdir}/init.d"

updatercd_postinst() {
if test "x$D" != "x"; then
	OPT="-r $D"
else
	OPT="-s"
fi
if type update-rc.d >/dev/null 2>/dev/null; then
	update-rc.d $OPT ${INITSCRIPT_NAME} ${INITSCRIPT_PARAMS}
fi
}

updatercd_prerm() {
if test "x$D" = "x"; then
	${INIT_D_DIR}/${INITSCRIPT_NAME} stop
fi
}

updatercd_postrm() {
if test "$D" != ""; then
	OPT="-f -r $D"
else
	OPT=""
fi
if type update-rc.d >/dev/null 2>/dev/null; then
	update-rc.d $OPT ${INITSCRIPT_NAME} remove
fi
}


def update_rc_after_parse(d):
    if d.getVar('INITSCRIPT_PACKAGES') == None:
        if d.getVar('INITSCRIPT_NAME') == None:
<<<<<<< HEAD
            raise bb.build.FuncFailed("%s inherits update-rc.d but doesn't set INITSCRIPT_NAME" % d.getVar('FILE'))
        if d.getVar('INITSCRIPT_PARAMS') == None:
            raise bb.build.FuncFailed("%s inherits update-rc.d but doesn't set INITSCRIPT_PARAMS" % d.getVar('FILE'))
=======
            raise bb.build.FuncFailed, "%s inherits update-rc.d but doesn't set INITSCRIPT_NAME" % d.getVar('FILE')
        if d.getVar('INITSCRIPT_PARAMS') == None:
            raise bb.build.FuncFailed, "%s inherits update-rc.d but doesn't set INITSCRIPT_PARAMS" % d.getVar('FILE')
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

python __anonymous() {
    update_rc_after_parse(d)
}

<<<<<<< HEAD
PACKAGESPLITFUNCS_prepend = "populate_packages_updatercd "

python populate_packages_updatercd () {
    def update_rcd_package(pkg):
        bb.debug(1, 'adding update-rc.d calls to postinst/postrm for %s' % pkg)
        """
        update_rc.d postinst is appended here because pkg_postinst may require to
        execute on the target. Not doing so may cause update_rc.d postinst invoked
        twice to cause unwanted warnings.
        """ 

=======
python populate_packages_prepend () {
    def update_rcd_package(pkg):
        bb.debug(1, 'adding update-rc.d calls to postinst/postrm for %s' % pkg)
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        localdata = bb.data.createCopy(d)
        overrides = localdata.getVar("OVERRIDES", True)
        localdata.setVar("OVERRIDES", "%s:%s" % (pkg, overrides))
        bb.data.update_data(localdata)

<<<<<<< HEAD
        postinst = d.getVar('pkg_postinst_%s' % pkg, True)
=======
        """
        update_rc.d postinst is appended here because pkg_postinst may require to
        execute on the target. Not doing so may cause update_rc.d postinst invoked
        twice to cause unwanted warnings.
        """ 
        postinst = localdata.getVar('pkg_postinst', True)
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        if not postinst:
            postinst = '#!/bin/sh\n'
        postinst += localdata.getVar('updatercd_postinst', True)
        d.setVar('pkg_postinst_%s' % pkg, postinst)

<<<<<<< HEAD
        prerm = d.getVar('pkg_prerm_%s' % pkg, True)
=======
        prerm = localdata.getVar('pkg_prerm', True)
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        if not prerm:
            prerm = '#!/bin/sh\n'
        prerm += localdata.getVar('updatercd_prerm', True)
        d.setVar('pkg_prerm_%s' % pkg, prerm)

<<<<<<< HEAD
        postrm = d.getVar('pkg_postrm_%s' % pkg, True)
=======
        postrm = localdata.getVar('pkg_postrm', True)
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        if not postrm:
                postrm = '#!/bin/sh\n'
        postrm += localdata.getVar('updatercd_postrm', True)
        d.setVar('pkg_postrm_%s' % pkg, postrm)

<<<<<<< HEAD
    # Check that this class isn't being inhibited (generally, by
    # systemd.bbclass) before doing any work.
    if "sysvinit" in d.getVar("DISTRO_FEATURES").split() or \
       not d.getVar("INHIBIT_UPDATERCD_BBCLASS", True):
        pkgs = d.getVar('INITSCRIPT_PACKAGES', True)
        if pkgs == None:
            pkgs = d.getVar('UPDATERCPN', True)
            packages = (d.getVar('PACKAGES', True) or "").split()
            if not pkgs in packages and packages != []:
                pkgs = packages[0]
        for pkg in pkgs.split():
            update_rcd_package(pkg)
=======
    pkgs = d.getVar('INITSCRIPT_PACKAGES', True)
    if pkgs == None:
        pkgs = d.getVar('UPDATERCPN', True)
        packages = (d.getVar('PACKAGES', True) or "").split()
        if not pkgs in packages and packages != []:
            pkgs = packages[0]
    for pkg in pkgs.split():
        update_rcd_package(pkg)
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
}
