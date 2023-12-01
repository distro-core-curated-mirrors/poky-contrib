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

INHIBIT_DEFAULT_DEPS = "1"
INHIBIT_AUTOTOOLS_DEPS = "1"

LICENSE = "FSF-Unlimited"
LIC_FILES_CHKSUM = "file://../COPYING;md5=4bd090a20bfcd1a18f1f79837b5e3e91"

inherit native

S = "${WORKDIR}/gettext-${PV}"

python get_aclocal_files() {
    fpath = oe.path.join(d.getVar("S"), "/gettext-tools/m4/Makefile.am")
    with open(fpath) as f:
        content = f.read()
        for l in content.replace("\\\n","").split("\n"):
            if l.startswith("aclocal_DATA"):
                aclocal_files = l.split("=")[1]
                with open(oe.path.join(d.getVar("WORKDIR"),"aclocal-files"),'w') as outf:
                    outf.write(aclocal_files)
                break
        else:
            bb.error("Could not obtain list of installed aclocal files from {}".format(fpath))
}
do_install[prefuncs] += "get_aclocal_files"

# can we just install the archive?!

do_install () {
	install -d ${D}${datadir}/aclocal/
	for i in `cat ${WORKDIR}/aclocal-files`; do
		cp ${S}/gettext-tools/m4/$i ${D}${datadir}/aclocal/
	done
	install -d ${D}${datadir}/gettext/po/
	cp ${S}/build-aux/config.rpath ${D}${datadir}/gettext/
	cp ${S}/gettext-runtime/po/Makefile.in.in ${D}${datadir}/gettext/po/
	cp ${S}/gettext-runtime/po/remove-potcdate.sin ${D}${datadir}/gettext/po/

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
    #install -D ${S}/gettext-tools/misc/autopoint.in ${D}${bindir}/autopoint
}
