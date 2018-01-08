SUMMARY = "Utilities and libraries for producing multi-lingual messages"
DESCRIPTION = "GNU gettext is a set of tools that provides a framework to help other programs produce multi-lingual messages. \
These tools include a set of conventions about how programs should be written to support message catalogs, a directory and file \
naming organization for the message catalogs themselves, a runtime library supporting the retrieval of translated messages, and \
a few stand-alone programs to massage in various ways the sets of translatable and already translated strings."
HOMEPAGE = "http://www.gnu.org/software/gettext/gettext.html"
SECTION = "libs"
LICENSE = "GPLv3+ & LGPL-2.1+"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"

DEPENDS = "gettext-native virtual/libiconv"
DEPENDS_class-native = "gettext-minimal-native"
PROVIDES = "virtual/gettext"
PROVIDES_class-native = "virtual/gettext-native"

SRC_URI = "${GNU_MIRROR}/gettext/gettext-${PV}.tar.gz \
	   file://parallel.patch \
	   file://add-with-bisonlocaledir.patch \
	   file://cr-statement.c-timsort.h-fix-formatting-issues.patch \
	   file://use-pkgconfig.patch \
"
SRC_URI[md5sum] = "97e034cf8ce5ba73a28ff6c3c0638092"
SRC_URI[sha256sum] = "ff942af0e438ced4a8b0ea4b0b6e0d6d657157c5e2364de57baa279c1c125c43"

inherit autotools texinfo pkgconfig

EXTRA_OECONF += "--without-lispdir \
                 --disable-csharp \
                 --disable-java \
                 --disable-native-java \
                 --disable-openmp \
                 --disable-acl \
                 --without-emacs \
                 --without-cvs \
                 --without-git \
                "
EXTRA_OECONF_append_class-target = " \
                 --with-bisonlocaledir=${datadir}/locale \
"

PACKAGECONFIG ??= "croco glib libxml"
PACKAGECONFIG_class-native = ""
PACKAGECONFIG_class-nativesdk = ""

PACKAGECONFIG[croco] = "--without-included-libcroco,--with-included-libcroco,libcroco"
PACKAGECONFIG[glib] = "--without-included-glib,--with-included-glib,glib-2.0"
PACKAGECONFIG[libxml] = "--without-included-libxml,--with-included-libxml,libxml2"
# Need paths here to avoid host contamination but this can cause RPATH warnings
# or problems if $libdir isn't $prefix/lib.
PACKAGECONFIG[libunistring] = "--with-libunistring-prefix=${STAGING_LIBDIR}/..,--with-included-libunistring,libunistring"
PACKAGECONFIG[msgcat-curses] = "--with-libncurses-prefix=${STAGING_LIBDIR}/..,--disable-curses,ncurses,"

AUTOTOOLS_SCRIPT_PATH = "${S}/gettext-tools"
acpaths = ""

PACKAGES =+ "libgettextlib libgettextsrc"
FILES_libgettextlib = "${libdir}/libgettextlib-*.so*"
FILES_libgettextsrc = "${libdir}/libgettextsrc-*.so*"

FILES_${PN} += "${libdir}/${BPN}/*"

# The its/Makefile.am has defined:
# itsdir = $(pkgdatadir)$(PACKAGE_SUFFIX)/its
# not itsdir = $(pkgdatadir), so use wildcard to match the version.
FILES_${PN} += "${datadir}/${BPN}-*/*"

do_install_append() {
    rm -f ${D}${libdir}/preloadable_libintl.so
}

do_install_append_class-native () {
	rm ${D}${datadir}/aclocal/*
	rm ${D}${datadir}/gettext/config.rpath
	rm ${D}${datadir}/gettext/po/Makefile.in.in
	rm ${D}${datadir}/gettext/po/remove-potcdate.sin

        create_wrapper ${D}${bindir}/msgfmt \
                GETTEXTDATADIR="${STAGING_DATADIR_NATIVE}/gettext-0.19.8/"

}

BBCLASSEXTEND = "native nativesdk"
