SUMMARY = "Minimal gettext for supporting native autoconf/automake"
DESCRIPTION = "Contains the m4 macros sufficient to support building \
autoconf/automake. This provides a significant build time speedup by \
the removal of gettext-native from most dependency chains (now only \
needed for gettext for the target)."
SRC_URI = "file://aclocal.tgz \
           file://config.rpath \
           file://Makefile.in.in \
           file://remove-potcdate.sin \
           file://COPYING \
           file://0001-PATCH-Disable-the-test-to-convert-euc-jp.patch \
           file://autopoint \
           file://archive.dir.tar.bz2;unpack=0 \
"

INHIBIT_DEFAULT_DEPS = "1"
INHIBIT_AUTOTOOLS_DEPS = "1"

LICENSE = "FSF-Unlimited"
LIC_FILES_CHKSUM = "file://COPYING;md5=4bd090a20bfcd1a18f1f79837b5e3e91"

inherit native

S = "${WORKDIR}"

do_install () {
	install -d ${D}${datadir}/aclocal/ ${D}${bindir} ${D}${datadir}/gettext/po/
	sed -e "s|FIXMESTAGINGDIRHOST|${STAGING_DIR_NATIVE}|g" <${WORKDIR}/autopoint >${D}${bindir}/autopoint
	chmod +x ${D}${bindir}/autopoint
	cp ${WORKDIR}/*.m4 ${D}${datadir}/aclocal/
	cp ${WORKDIR}/config.rpath ${D}${datadir}/gettext/
	cp ${WORKDIR}/archive.dir.tar.bz2 ${D}${datadir}/gettext/
	cp ${WORKDIR}/Makefile.in.in ${D}${datadir}/gettext/po/
	cp ${WORKDIR}/remove-potcdate.sin ${D}${datadir}/gettext/po/
}
