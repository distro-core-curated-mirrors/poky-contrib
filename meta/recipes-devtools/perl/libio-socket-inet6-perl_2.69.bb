DESCRIPTION = "IO::Socket::INET6 - Object interface for AF_INET|AF_INET6 domain sockets"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
RDEPENDS_${PN} += "perl-module-test-more libsocket6-perl perl-module-io-socket"
PR = "r1"

BBCLASSEXTEND = "native"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/S/SH/SHLOMIF/IO-Socket-INET6-${PV}.tar.gz"
SRC_URI[md5sum] = "12a80a5164a775294a9bf9c812fc3257"
SRC_URI[sha256sum] = "accd565643969d905e199e28e60e833213ccc2026c372432df01e49b044c3045"

LIC_FILES_CHKSUM = "file://README;beginline=21;endline=36;md5=80d30c8774697320c6aa548e51e080ab"

S = "${WORKDIR}/IO-Socket-INET6-${PV}"

inherit cpan

PACKAGE_ARCH = "all"
