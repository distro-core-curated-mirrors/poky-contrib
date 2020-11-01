DESCRIPTION = "Is a sphinx extension which outputs QtHelp document."
HOMEPAGE = "http://babel.edgewall.org/"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=942469df9305abb1c59e95f778310384"

SRC_URI[sha256sum] = "4c33767ee058b70dba89a6fc5c1892c0d57a54be67ddd3e7875a18d14cba5a72"

PYPI_PACKAGE = "sphinxcontrib-qthelp"

inherit pypi setuptools3

BBCLASSEXTEND = "native nativesdk"
