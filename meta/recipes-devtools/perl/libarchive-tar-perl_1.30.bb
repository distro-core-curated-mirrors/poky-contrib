DESCRIPTION = "Archive::Tar - Perl module for manipulations of tar archives"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
DEPENDS += "libio-zlib-perl-native"
RDEPENDS_${PN} += "libio-zlib-perl"
PR = "r7"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/K/KA/KANE/Archive-Tar-${PV}.tar.gz"
SRC_URI[md5sum] = "89604ea8fadc990c7bb668259dacb439"
SRC_URI[sha256sum] = "c456d5c73a57a567440bca5c138a549a21637aa2e4049228b5ba63cf68d75a1a"

LIC_FILES_CHKSUM = "file://lib/Archive/Tar.pm;beginline=1717;endline=1723;md5=788006bf2a49fe8ca512e37894c5dbb7"

S = "${WORKDIR}/Archive-Tar-${PV}"

inherit cpan

BBCLASSEXTEND = "native"