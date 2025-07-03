SUMMARY = "Python wrapper for the ls-qpack QPACK library"
DESCRIPTION = "pylsqpack is a wrapper around the ls-qpack library. It \
provides Python Decoder and Encoder objects to read or write HTTP/3 headers \
compressed with QPACK."
HOMEPAGE = "https://github.com/aiortc/pylsqpack"
LICENSE = "BSD-3-Clause & MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=9f900c41b9e212d68a890b9b516874ba \
                    file://vendor/ls-qpack/LICENSE;md5=6452724baebb05cc37e8a6fd6a827378"

SRC_URI[sha256sum] = "b67f711b3c8370d9f40f7f7f536aa6018d8900fa09fa49f72f0c3f13886cecda"

inherit pypi python_setuptools_build_meta ptest-python-pytest

PYPI_PACKAGE = "pylsqpack"
