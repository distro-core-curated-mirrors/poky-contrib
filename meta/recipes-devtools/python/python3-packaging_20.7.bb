SUMMARY = "Core utilities for Python packages"
DESCRIPTION = "Reusable core utilities for various Python Packaging \
interoperability specifications. \
\
This library provides utilities that implement the interoperability \
specifications which have clearly one correct behaviour (eg: PEP 440) or \
benefit greatly from having a single shared implementation (eg: PEP 425). \
\
The packaging project includes the following: version handling, specifiers, \
markers, requirements, tags, utilities."
HOMEPAGE = "https://github.com/pypa/packaging"
SECTION = "devel/python"
LICENSE = "Apache-2.0 & BSD"
LIC_FILES_CHKSUM = "file://LICENSE;md5=faadaedca9251a90b205c9167578ce91"

SRC_URI[sha256sum] = "05af3bb85d320377db281cf254ab050e1a7ebcbf5410685a9a407e18a1f81236"

inherit pypi setuptools3

BBCLASSEXTEND = "native"

DEPENDS += "${PYTHON_PN}-setuptools-scm-native"
RDEPENDS_${PN} += "${PYTHON_PN}-pyparsing"
