# TODO inc file with all the common bits

SUMMARY = "Utilities and libraries for producing multi-lingual messages"
DESCRIPTION = "GNU gettext is a set of tools that provides a framework to help other programs produce multi-lingual messages. \
These tools include a set of conventions about how programs should be written to support message catalogs, a directory and file \
naming organization for the message catalogs themselves, a runtime library supporting the retrieval of translated messages, and \
a few stand-alone programs to massage in various ways the sets of translatable and already translated strings."
HOMEPAGE = "http://www.gnu.org/software/gettext/gettext.html"
SECTION = "libs"
LICENSE = "GPLv3+ & LGPL-2.1+"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"

DEPENDS = "virtual/libiconv"

# Note that whilst this package *should* be a libintl provider, as no supported
# C libraries need a standalone libintl this support has bitrotted and may need
# fixing.
PROVIDES = "virtual/libintl"

SRC_URI = "${GNU_MIRROR}/gettext/gettext-${PV}.tar.gz"
SRC_URI[md5sum] = "97e034cf8ce5ba73a28ff6c3c0638092"
SRC_URI[sha256sum] = "ff942af0e438ced4a8b0ea4b0b6e0d6d657157c5e2364de57baa279c1c125c43"

inherit autotools gettext

S = "${WORKDIR}/gettext-${PV}"
AUTOTOOLS_SCRIPT_PATH = "${S}/gettext-runtime"
acpaths = ""

# TODO make asprintf a packageconfig. enable if this recipe barely gets used. put in own package.
EXTRA_OECONF += "--disable-csharp \
                 --disable-java \
                 --disable-native-java \
				 --disable-libasprintf \
                "

# gettext-runtime thinks musl wants this, but it doesn't. One day gettext won't
# install this for musl.
do_install_append_libc-musl () {
	rm -f ${D}${libdir}/charset.alias
}

# If the glibc has libintl then an empty $libdir is created, so delete it.
do_install_append() {
	rmdir --ignore-fail-on-non-empty ${D}${libdir}
}

FILES_${PN}-doc += "${datadir}/gettext/ABOUT-NLS"

BBCLASSEXTEND = "native nativesdk"
