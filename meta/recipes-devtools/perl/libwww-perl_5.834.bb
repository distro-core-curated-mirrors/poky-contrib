DESCRIPTION = "libwww-perl provides a simple and consistent API to the World Wide Web"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
DEPENDS = "liburi-perl-native libhtml-parser-perl-native libhtml-tagset-perl-native"
RDEPENDS_${PN} += " \
	libhtml-parser-perl \
	libhtml-tagset-perl \
	liburi-perl \
	perl-module-digest-md5 \
	perl-module-net-ftp \
	"

PR = "r1"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/libwww-perl-${PV}.tar.gz"
SRC_URI[md5sum] = "f2ed8a461f76556c9caed9087f47c86c"
SRC_URI[sha256sum] = "1a50eb91d1deeca3be10982e129e786809ad6f0f8049b156e91e889e5a7288ff"

LIC_FILES_CHKSUM = "file://README;beginline=87;endline=91;md5=d1294ffd182a35efd0c3982adeb533c0"

S = "${WORKDIR}/libwww-perl-${PV}"

inherit cpan

PACKAGE_ARCH = "all"

BBCLASSEXTEND = "native"