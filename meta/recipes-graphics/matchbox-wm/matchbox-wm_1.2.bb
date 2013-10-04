SECTION = "x11/wm"
DESCRIPTION = "Matchbox window manager"
LICENSE = "GPLv2.0+"
DEPENDS = "libmatchbox virtual/libx11 libxext libxcomposite libxfixes xdamage libxrender startup-notification expat"
PR = "r5"

<<<<<<< HEAD
SRC_URI = "http://downloads.yoctoproject.org/releases/matchbox/matchbox-window-manager/${PV}/matchbox-window-manager-${PV}.tar.bz2 \
=======
SRC_URI = "http://matchbox-project.org/sources/matchbox-window-manager/1.2/matchbox-window-manager-${PV}.tar.bz2 \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
           file://configure_fix.patch \
           file://kbdconfig \
           file://gconf-2.m4"

SRC_URI[md5sum] = "3e158dcf57823b55c926d95b245500fb"
SRC_URI[sha256sum] = "81a23a4af797cf350759fd5ac738797015a66dd5dba2f3d9f3c6908506c1ceff"

S = "${WORKDIR}/matchbox-window-manager-${PV}"

inherit autotools pkgconfig

FILES_${PN} = "${bindir}/* \
	       ${datadir}/matchbox \
	       ${sysconfdir}/matchbox \
	       ${datadir}/themes/blondie/matchbox \
	       ${datadir}/themes/Default/matchbox \
	       ${datadir}/themes/MBOpus/matchbox"

EXTRA_OECONF = " --enable-startup-notification \
                 --disable-xrm \
                 --enable-expat \
                 --with-expat-lib=${STAGING_LIBDIR} \
                 --with-expat-includes=${STAGING_INCDIR}"


do_configure_prepend () {
        cp ${WORKDIR}/gconf-2.m4 ${S}/
}

do_install_prepend() {
	install ${WORKDIR}/kbdconfig ${S}/data/kbdconfig
}
