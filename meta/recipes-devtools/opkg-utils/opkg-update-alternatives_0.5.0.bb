SUMMARY = "Utility for managing the alternatives system"
HOMEPAGE = "http://git.yoctoproject.org/cgit/cgit.cgi/opkg-utils"
LICENSE = "GPL-2.0-or-later"
LIC_FILES_CHKSUM = "file://COPYING;md5=94d55d512a9ba36caa9b7df079bae19f"

PROVIDES += "virtual/update-alternatives"

SRC_URI = "git://git.yoctoproject.org/opkg-utils;protocol=https;branch=master \
           file://0001-update-alternatives-correctly-match-priority.patch \
           "
SRCREV = "9239541f14a2529b9d01c0a253ab11afa2822dab"

S = "${WORKDIR}/git"

inherit allarch

do_compile() {
    :
}

do_install() {
    install -d ${D}${bindir}
    install update-alternatives ${D}${bindir}

    # Fix the hard-coded reference in the help output
    sed -i ${D}${bindir}/update-alternatives -e 's,/usr/bin,${bindir},g'
}

pkg_postrm:${PN} () {
	rm -rf $D${nonarch_libdir}/opkg/alternatives
	rmdir $D${nonarch_libdir}/opkg || true
}

BBCLASSEXTEND = "native nativesdk"

CLEANBROKEN = "1"
