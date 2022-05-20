SUMMARY = "A simple, correct PEP517 package builder"
HOMEPAGE = "https://github.com/pypa/build"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=310439af287b0fb4780b2ad6907c256c"

SRC_URI += "file://0001-infra-switch-to-flit.patch \
            file://0002-Replaced-the-use-of-pep517-with-pyproject-hooks-beca.patch"

SRC_URI[sha256sum] = "1a07724e891cbd898923145eb7752ee7653674c511378eb9c7691aab1612bc3c"

inherit pypi python_flit_core

DEPENDS += "python3-pyproject-hooks-native"

DEPENDS:remove:class-native = "python3-build-native"

PEP517_BUILD_OPTS:class-native = "--skip-dependency-check"

do_compile:prepend:class-native() {
    export PYTHONPATH="${S}/src"
}

RDEPENDS:${PN} += "python3-packaging python3-pyproject-hooks"

BBCLASSEXTEND = "native nativesdk"
