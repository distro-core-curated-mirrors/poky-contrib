DESCRIPTION = "Test::Pod - check for POD errors in files"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
BBCLASSEXTEND = "native"
RDEPENDS_${PN} += "perl-module-test-more perl-module-file-spec perl-module-module-build perl-module-pod-simple"
PR = "r1"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/D/DW/DWHEELER/Test-Pod-${PV}.tar.gz"
SRC_URI[md5sum] = "9c9b7ff52ea339aecbf247cd573df238"
SRC_URI[sha256sum] = "ea6de469a8db6549381e41095055bc3741aadf0d353aa1bd5b6e441bc500a79c"

LIC_FILES_CHKSUM = "file://README;beginline=28;endline=32;md5=f296e14bc9da636eb8e66af8ae355fcc"

S = "${WORKDIR}/Test-Pod-${PV}"

inherit cpan_build

PACKAGE_ARCH = "all"
