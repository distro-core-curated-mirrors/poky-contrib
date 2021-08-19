SUMMARY = "A library for property-based testing"
HOMEPAGE = "https://hypothesis.works/"
LICENSE = "MPL-2.0"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=4ee62c16ebd0f4f99d906f36b7de8c3c"

PYPI_PACKAGE = "hypothesis"
UPSTREAM_CHECK_URI ?= "https://pypi.org/project/${PYPI_PACKAGE}/"
UPSTREAM_CHECK_REGEX ?= "/${PYPI_PACKAGE}/(?P<pver>(\d+[\.\-_]*)+)/"

inherit ptest setuptools3

SRC_URI = " \
    git://github.com/HypothesisWorks/hypothesis.git;protocol=https;branch=master \
    file://run-ptest \
"
SRCREV = "1f0c8f4212b826d1fe61b2a82691753102a098bc"

S = "${WORKDIR}/git/hypothesis-python"

RDEPENDS:${PN} += " \
    python3-attrs \
    python3-compression \
    python3-core \
    python3-json \
    python3-sortedcontainers \
    python3-statistics \
    python3-unittest \
    "

RDEPENDS:${PN}-ptest += " \
    python3-profile \
    python3-pexpect \
    python3-pytest \
    python3-unixadmin \
    "

do_install_ptest() {
	install -d ${D}${PTEST_PATH}/tests
	cp -rf ${S}/tests/* ${D}${PTEST_PATH}/tests/
}

BBCLASSEXTEND = "native nativesdk"
