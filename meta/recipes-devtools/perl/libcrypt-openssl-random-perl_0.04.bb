DESCRIPTION = "Perl: random routines for Crypt::OpenSSL::RSA"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
DEPENDS = "openssl"
PR = "r1"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/I/IR/IROBERTS/Crypt-OpenSSL-Random-${PV}.tar.gz;name=crypt-openssl-random-perl-${PV}"
SRC_URI[crypt-openssl-random-perl-0.04.md5sum] = "c56ac5dbdd46122eb9b8da59613b7b0a"
SRC_URI[crypt-openssl-random-perl-0.04.sha256sum] = "acf7eb81023cd1f40d8c60b893096d041513df2be2aefe145cc7ae1a3dcc78c7"

LIC_FILES_CHKSUM = "file://LICENSE;md5=385c55653886acac3821999a3ccd17b3"

S = "${WORKDIR}/Crypt-OpenSSL-Random-${PV}"

inherit cpan

BBCLASSEXTEND = "native"