SECTION = "devel"
DESCRIPTION = "GNU multiprecision arithmetic library"
HOMEPAGE = "http://gmplib.org/"
LICENSE = "GPLv3 LGPLv3"

<<<<<<< HEAD
REVISION = ""

SRC_URI = "ftp://ftp.gmplib.org/pub/gmp-${PV}/gmp-${PV}${REVISION}.tar.bz2 \
=======
SRC_URI = "${GNU_MIRROR}/gmp/gmp-${PV}.tar.bz2 \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
	   file://configure.patch \
	   file://amd64.patch "

inherit autotools

ARM_INSTRUCTION_SET = "arm"

acpaths = ""

BBCLASSEXTEND = "native nativesdk"

EXTRA_OECONF += " --enable-cxx=detect"

PACKAGES =+ "libgmpxx"
FILES_libgmpxx = "${libdir}/libgmpxx${SOLIBS}"

SSTATE_SCAN_FILES += "gmp.h"
