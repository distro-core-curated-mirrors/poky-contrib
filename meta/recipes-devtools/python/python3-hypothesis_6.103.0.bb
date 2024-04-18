SUMMARY = "A library for property-based testing"
HOMEPAGE = "https://github.com/HypothesisWorks/hypothesis/tree/master/hypothesis-python"
LICENSE = "MPL-2.0"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=4ee62c16ebd0f4f99d906f36b7de8c3c"

inherit pypi setuptools3 ptest

SRC_URI += " \
    file://run-ptest \
    file://test_binary_search.py \
    file://test_rle.py \
    "

SRC_URI[sha256sum] = "7fe91917b99fc98ac150ec295775a687448c7c42c2276ab6e4a6969a4b285bb5"

RDEPENDS:${PN} += " \
    python3-attrs \
    python3-compression \
    python3-core \
    python3-json \
    python3-pytest \
    python3-sortedcontainers \
    python3-statistics \
    python3-unittest \
    "

RDEPENDS:${PN}-ptest += " \
    python3-unittest-automake-output \
    "

do_install_ptest() {
    install -d ${D}${PTEST_PATH}/examples
    install -m 0755 ${UNPACKDIR}/test_binary_search.py ${D}${PTEST_PATH}/examples/
    install -m 0755 ${UNPACKDIR}/test_rle.py ${D}${PTEST_PATH}/examples/
}

BBCLASSEXTEND = "native nativesdk"
