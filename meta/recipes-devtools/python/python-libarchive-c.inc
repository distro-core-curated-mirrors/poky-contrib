SUMMARY = "Python interface to libarchive"
HOMEPAGE = "https://github.com/Changaco/python-libarchive-c"
LICENSE = "CC0-1.0"
LIC_FILES_CHKSUM = "file://README.rst;beginline=56;endline=59;md5=6eb922dae7cb03b99ef214e4ae8d1f3f"

SRC_URI = "git://github.com/Changaco/python-libarchive-c.git;protocol=https"

PV = "2.7+git${SRCPV}"
SRCREV = "e1d8a23db90838f528aa59a6ace8ff8213e61c60"

S = "${WORKDIR}/git"

BBCLASSEXTEND = "native"
