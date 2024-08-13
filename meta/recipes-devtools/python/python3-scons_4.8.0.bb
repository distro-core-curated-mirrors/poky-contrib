SUMMARY = "Software Construction tool (make/autotools replacement)"
HOMEPAGE = "https://github.com/SCons/scons"
SECTION = "devel/python"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=d903b0b8027f461402bac9b5169b36f7"

SRC_URI[sha256sum] = "2c7377ff6a22ca136c795ae3dc3d0824696e5478d1e4940f2af75659b0d45454"

PYPI_PACKAGE = "SCons"

inherit pypi python_setuptools_build_meta

S = "${UNPACKDIR}/${PYPI_PACKAGE}-${PV}"

RDEPENDS:${PN}:class-target = "\
  python3-core \
  python3-compression \
  python3-db \
  python3-fcntl \
  python3-io \
  python3-json \
  python3-shell \
  python3-pickle \
  python3-pkg-resources \
  python3-pprint \
  "

do_install:append() {
    install -d ${D}${mandir}/man1
    cp ${S}/scons*.1 ${D}${mandir}/man1/
}

inherit manpages

# inherit manpages requires this to be present, however python3-scons does not have
# configuration options, and installs manpages always
PACKAGECONFIG[manpages] = ""

do_install:append:class-native() {
    create_wrapper ${D}${bindir}/scons SCONS_LIB_DIR='${STAGING_DIR_HOST}/${PYTHON_SITEPACKAGES_DIR}' PYTHONNOUSERSITE='1'
}

BBCLASSEXTEND = "native"
