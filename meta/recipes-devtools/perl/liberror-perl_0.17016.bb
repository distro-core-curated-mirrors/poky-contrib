DESCRIPTION = "Error - Error/exception handling in an OO-ish way"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
RDEPENDS_${PN} = " \
	 perl-module-scalar-util \
	 perl-module-warnings \
	 "

PR = "r1"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/S/SH/SHLOMIF/Error-${PV}.tar.gz;name=error-perl-${PV}"
SRC_URI[error-perl-0.17016.md5sum] = "eedcd3c6970568dd32092b5334328eff"
SRC_URI[error-perl-0.17016.sha256sum] = "f013a33ce33f324d6ff73ca074f34aa13f04bcec11e7f91c820c2e7b5e1979aa"

LIC_FILES_CHKSUM = "file://lib/Error.pm;beginline=3;endline=5;md5=ef1f6569dedd0baff828294836bc1b8e"

S = "${WORKDIR}/Error-${PV}"

inherit cpan

BBCLASSEXTEND="native"

PACKAGE_ARCH = "all"
