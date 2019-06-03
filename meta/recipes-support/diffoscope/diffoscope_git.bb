SUMMARY = "in-depth comparison of files, archives, and directories"
HOMEPAGE = "https://diffoscope.org/"
LICENSE = "GPL-3.0+"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"

SRC_URI = "\
    git://anonscm.debian.org/git/reproducible/diffoscope.git;protocol=https \
    file://0001-Skip-NOBITS-.eh_frame-ELF-sections.patch \
    "

UPSTREAM_CHECK_GITTAGREGEX = "(?P<pver>\d+)"

PV = "114+git${SRCPV}"
SRCREV = "d9dcdc017ef072284a29582178bce5de388d0869"
S = "${WORKDIR}/git"

do_install_append_class-native() {
        sed -i -e 's|^#!.*/usr/bin/env python|#! /usr/bin/env python|' ${D}${bindir}/diffoscope
}

inherit setuptools3

RDEPENDS_${PN} += "binutils vim squashfs-tools python3-libarchive-c python3-magic"

BBCLASSEXTEND = "native"
