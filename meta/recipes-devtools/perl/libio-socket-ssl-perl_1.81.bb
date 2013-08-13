DESCRIPTION = "IO::Socket::SSL -- Nearly transparent SSL encapsulation for IO::Socket::INET"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
RDEPENDS_${PN} += "perl-module-scalar-util libnet-ssleay-perl"
BBCLASSEXTEND = "native"
PR = "r1"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/S/SU/SULLR/IO-Socket-SSL-${PV}.tar.gz"
SRC_URI[md5sum] = "a29788f8c470778f8701a09134706108"
SRC_URI[sha256sum] = "3ee96f16ca4c4e1ce1bbd9a9e32bfeea3c1c635753caee86146afc7dec95e7ed"

LIC_FILES_CHKSUM = "file://lib/IO/Socket/SSL.pm;beginline=2613;endline=2614;md5=36e99aae7c844e5079db6a0b9a874b84"

S = "${WORKDIR}/IO-Socket-SSL-${PV}"

inherit cpan

PACKAGE_ARCH = "all"
