DESCRIPTION = "Compress::Zlib - Interface to zlib compression library"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
DEPENDS += "expat expat-native"
PR = "r2"

SRC_URI = "http://www.cpan.org/modules/by-module/IO/IO-Compress-Zlib-${PV}.tar.gz"

LIC_FILES_CHKSUM = "file://README;beginline=8;endline=10;md5=f8792c4c56e0e7d7660b4abd308ba58a"

S = "${WORKDIR}/IO-Compress-Zlib-${PV}"

EXTRA_CPANFLAGS = "EXPATLIBPATH=${STAGING_LIBDIR} EXPATINCPATH=${STAGING_INCDIR}"

inherit cpan

SRC_URI[md5sum] = "22f3b677a6f1782713c8451966598d3f"
SRC_URI[sha256sum] = "9d25ffdfacb3d43cbae618c68b62264aab2f56a9cf65ad2f974af9dcbae97669"

BBCLASSEXTEND = "native"