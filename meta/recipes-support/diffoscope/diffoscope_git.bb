SUMMARY = "in-depth comparison of files, archives, and directories"
HOMEPAGE = "https://diffoscope.org/"
LICENSE = "GPL-3.0+"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504 \
                    file://debian/copyright;md5=be438743f88244eb5e3ad99aca166ca2"

SRC_URI = "git://anonscm.debian.org/git/reproducible/diffoscope.git;protocol=https"

PV = "78+git${SRCPV}"
SRCREV = "dcfffcbb46685081b883d43ae9e4400ffa43c94c"
S = "${WORKDIR}/git"

DEPENDS_${PN} = "python3 python3-libarchive-c python3-magic"
DEPENDS_class-native = "python3-native python3-libarchive-c-native python3-magic-native"

do_install_append_class-native() {
        sed -i -e 's|^#!.*/usr/bin/env python|#! /usr/bin/env python|' ${D}${bindir}/diffoscope
}

inherit setuptools3

BBCLASSEXTEND = "native"
