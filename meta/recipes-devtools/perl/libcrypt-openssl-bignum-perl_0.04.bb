DESCRIPTION = "Perl interface to OpenSSL's multiprecision integer arithmetic"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
DEPENDS = "openssl"
PR = "r1"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/I/IR/IROBERTS/Crypt-OpenSSL-Bignum-${PV}.tar.gz"
SRC_URI[md5sum] = "9369ef722b0705c0604998559988eb18"
SRC_URI[sha256sum] = "73a1e3a2419054a5109629c55d3ec322415be07d6bb6029b830a30e8f1126fa3"

LIC_FILES_CHKSUM = "file://LICENSE;md5=385c55653886acac3821999a3ccd17b3"

S = "${WORKDIR}/Crypt-OpenSSL-Bignum-${PV}"

inherit cpan

BBCLASSEXTEND = "native"