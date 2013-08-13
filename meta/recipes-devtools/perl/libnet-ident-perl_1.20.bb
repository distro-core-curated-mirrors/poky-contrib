DESCRIPTION = "Net::Ident - lookup the username on the remote end of a TCP/IP connection"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
PR = "r1"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/J/JP/JPC/Net-Ident-${PV}.tar.gz"
SRC_URI[md5sum] = "70f265f46548675be01977d3c9eed570"
SRC_URI[sha256sum] = "c8370f21562c91d808ed37e105f95c5ba76b91d14186861d24832ccea094000c"

LIC_FILES_CHKSUM = "file://Ident.pm;beginline=917;endline=918;md5=6e31a6c8a954796facee858a1e8932cc"

S = "${WORKDIR}/Net-Ident-${PV}"

inherit cpan

PACKAGE_ARCH = "all"

BBCLASSEXTEND = "native"