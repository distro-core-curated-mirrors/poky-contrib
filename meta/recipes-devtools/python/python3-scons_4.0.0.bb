SUMMARY = "Software Construction tool (make/autotools replacement)"
HOMEPAGE = "https://github.com/SCons/scons"
SECTION = "devel/python"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=b94c6e2be9670c62b38f7118c12866d2"

SRC_URI[sha256sum] = "de8599189ee87bb84234e3d6e30bef0298d6364713979856927576b252c411f3"

PYPI_PACKAGE = "SCons"

inherit pypi setuptools3

RDEPENDS_${PN}_class-target = "\
  python3-core \
  python3-fcntl \
  python3-io \
  python3-json \
  python3-shell \
  python3-pickle \
  python3-pprint \
  python3-setuptools \
  "
