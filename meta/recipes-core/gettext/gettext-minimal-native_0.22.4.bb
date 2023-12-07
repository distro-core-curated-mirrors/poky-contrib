SUMMARY = "Minimal gettext for supporting native autoconf/automake"
DESCRIPTION = "Contains the m4 macros sufficient to support building \
autoconf/automake. This provides a significant build time speedup by \
the removal of gettext-native from most dependency chains (now only \
needed for gettext for the target)."

require gettext-sources.inc
# WHY?
SRC_URI += " \
           file://COPYING \
"

SRC_URI += "file://verbose.patch"

INHIBIT_DEFAULT_DEPS = "1"
INHIBIT_AUTOTOOLS_DEPS = "1"

LICENSE = "FSF-Unlimited"
LIC_FILES_CHKSUM = "file://../COPYING;md5=4bd090a20bfcd1a18f1f79837b5e3e91"

inherit native

S = "${WORKDIR}/gettext-${PV}"

do_install () {
    install -d ${D}${datadir}/gettext
    gzip --stdout ${S}/gettext-tools/misc/archive.dir.tar >${D}${datadir}/gettext/archive.dir.tar.gz

	install -d ${D}${bindir}
    sed \
        -e "s|@PACKAGE@|${PN}|g" \
        -e "s|@VERSION@|${PV}|g" \
        -e "s|@ARCHIVE_VERSION@|${PV}|g" \
        -e "s|@ARCHIVE_FORMAT@|dirgz|g" \
        -e "s|@prefix@|${prefix}|g" \
        -e "s|@exec_prefix@|${exec_prefix}|g" \
        -e "s|@bindir@|${bindir}|g" \
        -e "s|@datadir@|${datadir}|g" \
        -e "s|@datarootdir@|${datadir}|g" \
        -e "s|@PATH_SEPARATOR@|/|g" \
        <${S}/gettext-tools/misc/autopoint.in >${D}${bindir}/autopoint
    chmod +x ${D}${bindir}/autopoint
}
