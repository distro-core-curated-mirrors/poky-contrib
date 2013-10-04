DESCRIPTION = "Common X11 scripts and configuration files"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=751419260aa954499f7abaabaa882bbe"
SECTION = "x11"
PR = "r47"

SRC_URI = "file://etc \
           file://gplv2-license.patch"

S = "${WORKDIR}"
<<<<<<< HEAD
=======

inherit allarch
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

do_install() {
	cp -R ${S}/etc ${D}${sysconfdir}
	chmod -R 755 ${D}${sysconfdir}
	find ${D}${sysconfdir} -type f -name \*~ -exec rm -rf {} \;
}

RDEPENDS_${PN} = "dbus-x11 xmodmap xdpyinfo xtscal xinit formfactor"

