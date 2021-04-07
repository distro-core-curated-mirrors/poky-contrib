SUMMARY = "A set of tools for working with the Test Anything Protocol (TAP) in Python"
HOMEPAGE = "https://github.com/python-tap/tappy"
SECTION = "devel/python"
LICENSE = "BSD-2-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=44f4aeb3f15b2282170576107b16fa64"

PYPI_PACKAGE = "tap.py"

inherit pypi setuptools3

DEPENDS += "python3-babel-native"

SRC_URI[sha256sum] = "f5eeeeebfd64e53d32661752bb4c288589a3babbb96db3f391a4ec29f1359c70"

BBCLASSEXTEND = "native nativesdk"

RDEPENDS_${PN} += "python3-io python3-pkg-resources python3-stringold python3-unittest"
# These are for TAP13 parsing
RRECOMMENDS_${PN} += "python3-pyyaml python3-more-itertools"
