SUMMARY = "Read metadata from Python packages"
HOMEPAGE = "https://pypi.org/project/importlib-metadata/"
LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=3b83ef96387f14655fc854ddc3c6bd57"

SRC_URI[sha256sum] = "188bd24e4c346d3f0a933f275c2fec67050326a856b9a359881d7c2a697e8812"

inherit pypi python_setuptools_build_meta

PYPI_PACKAGE = "importlib_metadata"
DEPENDS += "python3-setuptools-scm-native"
RDEPENDS:${PN} += "python3-zipp python3-typing-extensions"

inherit ptest

SRC_URI += " \
    file://run-ptest \
"

RDEPENDS:${PN}-ptest += " \
    python3-pytest \
    python3-unittest-automake-output \
"

do_install_ptest() {
    install -d ${D}${PTEST_PATH}/tests
    cp -rf ${S}/tests/* ${D}${PTEST_PATH}/tests/
}

BBCLASSEXTEND = "native nativesdk"
