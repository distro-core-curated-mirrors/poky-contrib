SUMMARY = "Simple, fast, extensible JSON encoder/decoder for Python"
HOMEPAGE = "https://cheeseshop.python.org/pypi/simplejson"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=c6338d7abd321c0b50a2a547e441c52e"

SRC_URI[sha256sum] = "e64139b4ec4f1f24c142ff7dcafe55a22b811a74d86d66560c8815687143037d"

inherit pypi setuptools3 ptest-python-pytest

RDEPENDS:${PN} += "\
    python3-io \
    python3-netserver \
    python3-numbers \
"

# The ptests are in sniffio/_tests and not isolated
PTEST_PYTEST_DIR = "simplejson"

# No sense installing tests on target
do_install:append () {
    rm -rf ${D}${PYTHON_SITEPACKAGES_DIR}/simplejson/tests
	rm -rf ${D}${PYTHON_SITEPACKAGES_DIR}/simplejson/tool.py
}

BBCLASSEXTEND = "native nativesdk"


