SUMMARY = "Sniff out which async library your code is running under"
DESCRIPTION = "You’re writing a library. You’ve decided to be ambitious, \
and support multiple async I/O packages, like Trio, and asyncio, and … \
You’ve written a bunch of clever code to handle all the differences. But… \
how do you know which piece of clever code to run?"
HOMEPAGE = "https://github.com/python-trio/sniffio"
SECTION = "devel/python"
LICENSE = "MIT | Apache-2.0"
LIC_FILES_CHKSUM = "\
    file://LICENSE;md5=fa7b86389e58dd4087a8d2b833e5fe96 \
    file://LICENSE.MIT;md5=e62ba5042d5983462ad229f5aec1576c \
    file://LICENSE.APACHE2;md5=3b83ef96387f14655fc854ddc3c6bd57 \
"

inherit pypi python_setuptools_build_meta ptest-python-pytest

SRC_URI[sha256sum] = "f4324edc670a0f49750a81b895f35c3adb843cca46f0530f79fc1babb23789dc"

DEPENDS += "\
    python3-setuptools-scm-native \
"

RDEPENDS:${PN} += " \
    python3-numbers \
    python3-core \
"

# The ptests are in sniffio/_tests and not isolated
PTEST_PYTEST_DIR = "sniffio"

# No sense installing _tests on target
do_install:append () {
    rm -rf ${D}${PYTHON_SITEPACKAGES_DIR}/sniffio/_tests
}
