# The list of config scripts to mangle, for example ${bindir}/foo-config.
BINCONFIG ?= "${bindir}/*-config"

FILES_${PN}-dev += "${BINCONFIG}"

expand_glob() {
	# $1 is search base
	# $2 onwards is a list of globs
	RESULTS=""
	BASE=$1
    shift
	for PATTERN in "$@"; do
        RESULTS="$RESULTS $(ls $BASE$PATTERN 2>/dev/null)"
	done
	echo $RESULTS
}

PACKAGE_PREPROCESS_FUNCS += "binconfig_package_preprocess"
binconfig_package_preprocess () {
	for config in `expand_glob ${PKGD} ${BINCONFIG}`; do
		bbdebug 1 "Replacing paths in $config"
		sed -i \
			-e 's:${STAGING_BASELIBDIR}:${base_libdir}:g;' \
			-e 's:${STAGING_LIBDIR}:${libdir}:g;' \
			-e 's:${STAGING_INCDIR}:${includedir}:g;' \
			-e 's:${STAGING_DATADIR}:${datadir}:' \
			-e 's:${STAGING_DIR_HOST}${prefix}:${prefix}:' \
			-e 's:${STAGING_BINDIR_CROSS}:${bindir}:' \
			$config
	done
}


# The namespaces can clash here hence the two step replace
def get_binconfig_mangle(d):
    s = "-e ''"
    if not bb.data.inherits_class('native', d):
        optional_quote = r"\(\"\?\)"
        s += " -e 's:=%s${base_libdir}:=\\1OEBASELIBDIR:;'" % optional_quote
        s += " -e 's:=%s${libdir}:=\\1OELIBDIR:;'" % optional_quote
        s += " -e 's:=%s${includedir}:=\\1OEINCDIR:;'" % optional_quote
        s += " -e 's:=%s${datadir}:=\\1OEDATADIR:'" % optional_quote
        s += " -e 's:=%s${prefix}/:=\\1OEPREFIX/:'" % optional_quote
        s += " -e 's:=%s${exec_prefix}/:=\\1OEEXECPREFIX/:'" % optional_quote
        s += " -e 's:-L${libdir}:-LOELIBDIR:;'"
        s += " -e 's:-I${includedir}:-IOEINCDIR:;'"
        s += " -e 's:-L${WORKDIR}:-LOELIBDIR:'"
        s += " -e 's:-I${WORKDIR}:-IOEINCDIR:'"
        s += " -e 's:OEBASELIBDIR:${STAGING_BASELIBDIR}:;'"
        s += " -e 's:OELIBDIR:${STAGING_LIBDIR}:;'"
        s += " -e 's:OEINCDIR:${STAGING_INCDIR}:;'"
        s += " -e 's:OEDATADIR:${STAGING_DATADIR}:'"
        s += " -e 's:OEPREFIX:${STAGING_DIR_HOST}${prefix}:'"
        s += " -e 's:OEEXECPREFIX:${STAGING_DIR_HOST}${exec_prefix}:'"
        if d.getVar("OE_BINCONFIG_EXTRA_MANGLE", False):
            s += d.getVar("OE_BINCONFIG_EXTRA_MANGLE")

    return s

SYSROOT_PREPROCESS_FUNCS += "binconfig_sysroot_preprocess"
binconfig_sysroot_preprocess () {
	for config in `expand_glob ${D} ${BINCONFIG}`; do
		bbdebug 1 "Replacing paths in $config"
		configname=`basename $config`
		install -d ${SYSROOT_DESTDIR}${bindir_crossscripts}
		sed ${@get_binconfig_mangle(d)} $config > ${SYSROOT_DESTDIR}${bindir_crossscripts}/$configname
		chmod u+x ${SYSROOT_DESTDIR}${bindir_crossscripts}/$configname
	done
}

python () {
    if d.getVar("BINCONFIG_GLOB"):
        bb.error("BINCONFIG_GLOB is set, please use BINCONFIG instead")
    if not d.getVar("BINCONFIG"):
        bb.error("binconfig.bbclass inherited but BINCONFIG not set")
}
