DESCRIPTION = "HTML Tagset bits."
SECTION = "libs"
LICENSE = "Artistic-1.0 | GPLv1+"
PR = "r3"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/P/PE/PETDANCE/HTML-Tagset-${PV}.tar.gz"

S = "${WORKDIR}/HTML-Tagset-${PV}"

LIC_FILES_CHKSUM = "file://README;beginline=62;endline=66;md5=aa91eed6adfe182d2af676954f06a7c9"

inherit cpan

BBCLASSEXTEND="native"

SRC_URI[md5sum] = "d2bfa18fe1904df7f683e96611e87437"
SRC_URI[sha256sum] = "adb17dac9e36cd011f5243881c9739417fd102fce760f8de4e9be4c7131108e2"
