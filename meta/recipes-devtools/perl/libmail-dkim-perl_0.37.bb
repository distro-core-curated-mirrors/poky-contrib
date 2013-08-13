DESCRIPTION = "Mail::DKIM - Signs/verifies Internet mail with DKIM/DomainKey signatures"
SECTION = "libs"
LICENSE = "BSD"
DEPENDS = " \
	libcrypt-openssl-rsa-perl-native \
	libmailtools-perl-native \
	libnet-dns-perl-native \
	"
#	libdigest-sha-native
	
RDEPENDS_${PN} += " \
	libcrypt-openssl-rsa-perl \
	liberror-perl \
	libmailtools-perl \
	libnet-dns-perl \
	"
#	libdigest-sha
	
BBCLASSEXTEND = "native"
PR = "r1"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/J/JA/JASLONG/Mail-DKIM-${PV}.tar.gz;name=mail-dkim-perl-${PV}"
SRC_URI[mail-dkim-perl-0.37.md5sum] = "f3e84ec6b5e42d4cbcc7c42ea2900649"
SRC_URI[mail-dkim-perl-0.37.sha256sum] = "287173596f2e4ad4a44385d7ebbf868114d52ce73bd8d931b8dcf5c5ce19ad0b"

LIC_FILES_CHKSUM = "file://README;beginline=49;endline=53;md5=19e68eeff018b44a9601e97d1826bf89"

S = "${WORKDIR}/Mail-DKIM-${PV}"

inherit cpan

PACKAGE_ARCH = "all"
