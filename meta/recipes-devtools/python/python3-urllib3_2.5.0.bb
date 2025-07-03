SUMMARY = "Python HTTP library with thread-safe connection pooling, file post support, sanity friendly, and more"
HOMEPAGE = "https://github.com/urllib3/urllib3"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=52d273a3054ced561275d4d15260ecda"

SRC_URI[sha256sum] = "3fc47733c7e419d4bc3f6b3dc2b4f890bb743906a30d56ba4a5bfa4bbff92760"

inherit pypi python_hatchling ptest-python-pytest

PTEST_PYTEST_DIR = "test"

DEPENDS += " \
    python3-hatch-vcs-native \
"

RDEPENDS:${PN} += "\
    python3-certifi \
    python3-cryptography \
    python3-email \
    python3-idna \
    python3-json \
    python3-netclient \
    python3-pyopenssl \
    python3-threading \
    python3-logging \
"

RDEPENDS:${PN}-ptest += "\
    python3-httpx \
    python3-pysocks \
    python3-quart \
    python3-quart-trio \
    python3-trio \
    python3-trustme \
    python3-zoneinfo \
"

do_install_ptest:append () {
  cp -r ${S}/dummyserver ${D}${PTEST_PATH}
}

CVE_PRODUCT = "urllib3"

BBCLASSEXTEND = "native nativesdk"
