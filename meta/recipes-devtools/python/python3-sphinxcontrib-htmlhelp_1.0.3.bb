DESCRIPTION = "sphinxcontrib-htmlhelp is a sphinx extension which renders HTML help files"
HOMEPAGE = "https://www.sphinx-doc.org"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=942469df9305abb1c59e95f778310384"

SRC_URI[sha256sum] = "e8f5bb7e31b2dbb25b9cc435c8ab7a79787ebf7f906155729338f3156d93659b"

PYPI_PACKAGE = "sphinxcontrib-htmlhelp"

inherit pypi setuptools3

BBCLASSEXTEND = "native nativesdk"
