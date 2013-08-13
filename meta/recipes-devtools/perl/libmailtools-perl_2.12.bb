DESCRIPTION = "MailTools is a set of Perl modules related to mail applications"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
DEPENDS = " \
	libtest-pod-perl-native \
	libtimedate-perl-native \
	"	
RDEPENDS_${PN} += " \
	libtest-pod-perl \
	libtimedate-perl \
	perl-module-io-handle \
	perl-module-net-smtp \
	perl-module-test-more \
	"
BBCLASSEXTEND = "native"
PR = "r1"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/M/MA/MARKOV/MailTools-${PV}.tar.gz"
SRC_URI[md5sum] = "b233a5723a0f5680d8ddd4dfdcb14c14"
SRC_URI[sha256sum] = "51ad50f324a1d11df21c430ced74b2077c2cf5e2c27f263a181cbd9a5d964737"

LIC_FILES_CHKSUM = "file://lib/Mail/Address.pod;beginline=144;endline=149;md5=ecd68ad8c72392be4f4b325704f159a0"

S = "${WORKDIR}/MailTools-${PV}"

inherit cpan

PACKAGE_ARCH = "all"
