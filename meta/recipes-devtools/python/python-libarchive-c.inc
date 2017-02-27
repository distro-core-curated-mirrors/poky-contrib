SUMMARY = "Python interface to libarchive"
HOMEPAGE = "https://github.com/Changaco/python-libarchive-c"
LICENSE = "CC0-1.0"
LIC_FILES_CHKSUM = "file://README.rst;beginline=56;endline=59;md5=6eb922dae7cb03b99ef214e4ae8d1f3f"

SRC_URI = "git://github.com/Changaco/python-libarchive-c.git;protocol=https"

UPSTREAM_CHECK_GITTAGREGEX = "(?P<pver>\d+(\.\d+)+)"

PV = "2.8+git${SRCPV}"
SRCREV = "3894218b28b1daefa8417482273ce56c2c3f6b8e"

S = "${WORKDIR}/git"

RDEPENDS_${PN} += "libarchive"

BBCLASSEXTEND = "native"
