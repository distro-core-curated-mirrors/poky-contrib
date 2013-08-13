DESCRIPTION = "IP::Country - fast lookup of country codes from IP addresses"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
RDEPENDS_${PN} += "perl-module-extutils-makemaker"
BBCLASSEXTEND = "native"
PR = "r1"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/N/NW/NWETTERS/IP-Country-${PV}.tar.gz;name=ip-country-perl-${PV}"
SRC_URI[ip-country-perl-2.27.md5sum] = "32932280ee4729145e85e08dad5ab8c6"
SRC_URI[ip-country-perl-2.27.sha256sum] = "39ed6d3890d655159e950f785f5e124b580ebaa0ab531bc4cf182184801192e1"

LIC_FILES_CHKSUM = "file://lib/IP/Country.pm;beginline=149;endline=206;md5=1878c6d29ab55d9eb8ccc5842100e1c5"

S = "${WORKDIR}/IP-Country-${PV}"

inherit cpan

PACKAGE_ARCH = "all"
