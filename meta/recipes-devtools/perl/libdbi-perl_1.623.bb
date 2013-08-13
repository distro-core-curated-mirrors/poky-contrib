DESCRIPTION = "Various MIME modules."
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
PR = "r3"

RDEPENDS_${PN} = "perl-module-scalar-util \
            perl-module-file-spec \
            perl-module-storable \
            perl-module-test-simple"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/T/TI/TIMB/DBI-${PV}.tar.gz"

S = "${WORKDIR}/DBI-${PV}"

LIC_FILES_CHKSUM = "file://DBI.pm;beginline=8127;endline=8131;md5=7d9e154a9ca3c093d2422f7c692d5861"

inherit cpan

BBCLASSEXTEND="native"

SRC_URI[md5sum] = "b45654dca3b495f3d496c359f0029d96"
SRC_URI[sha256sum] = "912d73f9eb0601f592aa58897d9c6787e238d9780f30ac86059c83b7085de3a1"