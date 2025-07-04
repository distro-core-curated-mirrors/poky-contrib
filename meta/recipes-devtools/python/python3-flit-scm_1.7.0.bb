SUMMARY = "A PEP 518 build backend that uses setuptools_scm and flit_core."
DESCRIPTION = "A PEP 518 build backend that uses setuptools_scm to generate \
a version file from your version control system, then flit to build the package."
HOMEPAGE = "https://gitlab.com/WillDaSilva/flit_scm"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=80f451d0892e64764fe22dbd241b5f02"

SRC_URI[sha256sum] = "961bd6fb24f31bba75333c234145fff88e6de0a90fc0f7e5e7c79deca69f6bb2"

inherit pypi python_flit_scm_buildapi

PYPI_PACKAGE = "flit_scm"

do_compile:class-native () {
    python_flit_scm_buildapi_do_manual_build
}

do_install:class-native () {
    python_pep517_do_bootstrap_install
}

BBCLASSEXTEND = "native nativesdk"
