SUMMARY = "Free Implementation of the Unicode Bidirectional Algorithm"
SECTION = "libs"
LICENSE = "LGPLv2.1+"
LIC_FILES_CHKSUM = "file://COPYING;md5=a916467b91076e631dd8edb7424769c7"

SRC_URI = "https://github.com/${BPN}/${BPN}/releases/download/v${PV}/${BP}.tar.xz \
           file://run-ptest"
           "
SRC_URI[md5sum] = "97c87da9930e8e70fbfc8e2bcd031554"
SRC_URI[sha256sum] = "7f1c687c7831499bcacae5e8675945a39bacbad16ecaa945e9454a32df653c01"

UPSTREAM_CHECK_URI = "https://github.com/${BPN}/${BPN}/releases"

inherit meson lib_package pkgconfig ptest

CVE_PRODUCT = "gnu_fribidi fribidi"

do_install_ptest() {
    install -m755 ${S}/test/test-runner.py ${D}${PTEST_PATH}
    install -m644 ${S}/test/*.input ${S}/test/*.reference ${D}${PTEST_PATH}
    sed -i -e 's|@BINDIR@|${bindir}|g' -e 's|@PTEST_PATH@|${PTEST_PATH}|g' ${D}${PTEST_PATH}/run-ptest
}

RDEPENDS_${PN}-ptest += "${PN}-bin python3-core"

BBCLASSEXTEND = "native nativesdk"
