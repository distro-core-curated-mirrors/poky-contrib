DESCRIPTION = "Net::DNS - Perl interface to the DNS resolver"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
RDEPENDS_${PN} += " \
	libdigest-hmac-perl \
	libnet-ip-perl \
	perl-module-io-socket \
	perl-module-mime-base64 \
	perl-module-test-more \
	"
#	libdigest-sha 
	
BBCLASSEXTEND = "native"

PR = "r1"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/O/OL/OLAF/Net-DNS-${PV}.tar.gz;name=net-dns-perl-${PV}"
SRC_URI[net-dns-perl-0.66.md5sum] = "1635d876324e3c2f6e277d5778bfe94c"
SRC_URI[net-dns-perl-0.66.sha256sum] = "ee922a6ab1403820ad476713d62cb35e7092585ebd628f02865827fcb09d6823"

S = "${WORKDIR}/Net-DNS-${PV}"

LIC_FILES_CHKSUM = "file://README;beginline=278;endline=279;md5=ad22f8e011314590ae5991cfdcb35350"

inherit cpan
