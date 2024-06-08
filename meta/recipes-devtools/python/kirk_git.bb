SUMMARY = "All-in-one Linux Testing Framework"
HOMEPAGE = "https://github.com/acerv/kirk"
LICENSE = "GPL-2.0-only & LGPL-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=39bba7d2cf0ba1036f2a6e2be52fe3f0"

SRC_URI = "git://github.com/linux-test-project/kirk.git;protocol=https;branch=master"

PV = "1.2+git"
SRCREV = "bcb2df815d3fdbca470c1ff6ab14ac9cb2f9e3b7"

S = "${WORKDIR}/git"

inherit setuptools3 ptest

PACKAGECONFIG ?= "ssh ltx"
PACKAGECONFIG[ssh] = ",,,python3-asyncssh"
PACKAGECONFIG[ltx] = ",,,python3-msgpack"

RDEPENDS:${PN}:append:class-target = "\
    python3-asyncio \
    python3-core \
    python3-json \
    python3-logging \
    python3-netclient \
    python3-shell \
    python3-stringold \
"

SRC_URI += " \
    file://run-ptest \
"

RDEPENDS:${PN}-ptest += " \
    python3-pytest \
    python3-unittest-automake-output \
"

do_install_ptest() {
    install -d ${D}${PTEST_PATH}/libkirk/tests
    cp -rf ${S}/libkirk/tests/* ${D}${PTEST_PATH}/libkirk/tests/
}
