# Copyright (C) 2018 Joshua Watt <JPEWhacker@gmail.com>
# Released under the MIT license (see COPYING.MIT for the terms)

SUMMARY = "performs basic checks for the presence of bashisms"
HOMEPAGE = "https://salsa.debian.org/debian/devscripts"
LICENSE = "GPLv2"
SECTION = "devel"
LIC_FILES_CHKSUM = "file://COPYING;md5=faa39cbd7a7cded9a1436248295de3c2"

SRC_URI = "git://salsa.debian.org/debian/devscripts.git;protocol=https;branch=${BRANCH} \
    file://0001-checkbashisms.pl-Invoke-perl-from-PATH.patch \
    "

SRCREV = "77ecff2e9b18c74e8391aa0c8dccdd86a50544d5"

BRANCH = "master"

UPSTREAM_CHECK_GITTAGREGEX = "v(?P<ver>\d+(\.\d+)+)"

S = "${WORKDIR}/git"

inherit allarch

do_configure() {
}

do_compile() {
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${S}/scripts/checkbashisms.pl ${D}${bindir}
    sed -e "s@###VERSION###@${PV}@" -i ${D}${bindir}/checkbashisms.pl
}

RDEPENDS_${PN} = "perl"

BBCLASSEXTEND = "native"
