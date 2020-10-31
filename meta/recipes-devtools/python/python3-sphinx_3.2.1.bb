DESCRIPTION = "Python documentation generator"
HOMEPAGE = "http://sphinx-doc.org/"
SECTION = "devel/python"
LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://LICENSE;md5=cc3ed00294f08c93200bc064c73c9d40"

PYPI_PACKAGE = "Sphinx"

SRC_URI[sha256sum] = "321d6d9b16fa381a5306e5a0b76cd48ffbc588e6340059a729c6fdd66087e0e8"

inherit setuptools3 pypi

RDEPENDS:${PN} = "\
    python3-packaging python3-docutils python3-requests \
    python3-imagesize python3-alabaster python3-jinja2 \
    python3-babel python3-pygments python3-snowballstemmer \
    python3-sphinxcontrib-applehelp python3-sphinxcontrib-devhelp \
    python3-sphinxcontrib-jsmath python3-sphinxcontrib-htmlhelp \
    python3-sphinxcontrib-serializinghtml python3-sphinxcontrib-qthelp \
    "

BBCLASSEXTEND = "native nativesdk"
