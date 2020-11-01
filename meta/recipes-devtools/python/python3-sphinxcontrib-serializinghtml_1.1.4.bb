DESCRIPTION = 'sphinxcontrib-serializinghtml is a sphinx extension which outputs "serialized" HTML files (json and pickle).'
HOMEPAGE = "https://www.sphinx-doc.org"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=32a84ac5cd3bbd10c4d479233ad588b6"

SRC_URI[sha256sum] = "eaa0eccc86e982a9b939b2b82d12cc5d013385ba5eadcc7e4fed23f4405f77bc"

PYPI_PACKAGE = "sphinxcontrib-serializinghtml"

inherit pypi setuptools3

BBCLASSEXTEND = "native nativesdk"
