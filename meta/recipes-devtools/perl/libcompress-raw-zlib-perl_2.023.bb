DESCRIPTION = "Compress::Raw::Zlib - Perl Low-Level Interface to zlib compression library"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+ | zlib"
DEPENDS += "expat expat-native"
PR = "r1"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/Compress-Raw-Zlib-${PV}.tar.gz"

S = "${WORKDIR}/Compress-Raw-Zlib-${PV}"

EXTRA_CPANFLAGS = "EXPATLIBPATH=${STAGING_LIBDIR} EXPATINCPATH=${STAGING_INCDIR}"

inherit cpan

#FILES_${PN} = "${PERLLIBDIRS}/auto ${PERLLIBDIRS}/Compress ${datadir}/perl5"

SRC_URI[md5sum] = "3e2ce271f1eada6d192f424a1168b24c"
SRC_URI[sha256sum] = "ec74b8d04e823ae40602b87c01c230a7c91979a06efcc2f672aceb7f2196128a"

LIC_FILES_CHKSUM = "file://README;beginline=8;endline=17;md5=8783b40f014bf2c7db3843491242648e"

BBCLASSEXTEND = "native"