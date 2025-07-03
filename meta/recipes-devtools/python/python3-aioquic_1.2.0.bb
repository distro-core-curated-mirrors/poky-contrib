SUMMARY = "An implementation of QUIC and HTTP/3"
DESCRIPTION = "aioquic is a library for the QUIC network protocol in \
Python. It features a minimal TLS 1.3 implementation, a QUIC stack and \
an HTTP/3 stack."
HOMEPAGE = "https://github.com/aiortc/aioquic"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=71ae49675fda51bacc4b161ee66f15c3 \
                    file://docs/license.rst;md5=2ac99589e1d6fa6df5274445a72da612"

SRC_URI[sha256sum] = "f91263bb3f71948c5c8915b4d50ee370004f20a416f67fab3dcc90556c7e7199"

inherit pypi python_setuptools_build_meta ptest-python-pytest

RDEPENDS:${PN} = " \
    python3-certifi \
    python3-cryptography \
    python3-pylsqpack \
    python3-pyopenssl \
    python3-service-identity \
"
