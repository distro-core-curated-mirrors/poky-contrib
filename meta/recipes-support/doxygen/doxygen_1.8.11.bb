SUMMARY = "Doxygen is the de facto standard tool for generating documentation from annotated C++ sources"
DESCRIPTION = "Doxygen can generate an on-line documentation browser (in HTML) and/or an off-line \
               reference manual (in LaTeX) from a set of documented source files. There is also \
               support for generating output in RTF (MS-Word), PostScript, hyperlinked PDF, compressed \
               HTML, and Unix man pages. The documentation is extracted directly from the sources, \
               which makes it much easier to keep the documentation consistent with the source code. "
HOMEPAGE = "http://www.stack.nl/~dimitri/doxygen/"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://LICENSE;md5=b380c86cea229fa42b9e543fc491f5eb"

inherit cmake pythonnative

SRC_URI = "http://ftp.stack.nl/pub/users/dimitri/${BPN}-${PV}.src.tar.gz"
SRC_URI[md5sum] = "f4697a444feaed739cfa2f0644abc19b"
SRC_URI[sha256sum] = "65d08b46e48bd97186aef562dc366681045b119e00f83c5b61d05d37ea154049"

UPSTREAM_CHECK_URI = "http://www.stack.nl/~dimitri/doxygen/download.html"

BBCLASSEXTEND = "native"

# Cmake seems to look for include files only in sysroots, and fails
# when the include file comes from host's glibc
EXTRA_OECMAKE_class-native = "-DICONV_INCLUDE_DIR=/usr/include"
