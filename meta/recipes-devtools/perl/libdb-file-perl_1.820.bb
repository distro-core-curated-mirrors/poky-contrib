DESCRIPTION = "Perl5 access to Berkeley DB version 1.x"
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
DEPENDS = "virtual/db"
RDEPENDS_${PN} += "perl-module-extutils-makemaker"
PR = "r1"

BBCLASSEXTEND = "native"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/DB_File-${PV}.tar.gz"
SRC_URI[md5sum] = "28979bee29d8075b0dffab02fe29df6e"
SRC_URI[sha256sum] = "eae8d2d2144504118773f3e1787321d2c757e7c5abf0a60591c73495352ddf4a"

LIC_FILES_CHKSUM = "file://README;beginline=7;endline=9;md5=bf4016d4858a34cf7463229792033fc4"

S = "${WORKDIR}/DB_File-${PV}"

do_configure_prepend() {
	export DB_FILE_LIB=${STAGING_LIBDIR}
}

inherit cpan
