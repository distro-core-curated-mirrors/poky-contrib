FILES_${PN}-dev += "${bindir}/*-config"
 
# The namespaces can clash here hence the two step replace
def get_binconfig_mangle(d):
    s = "-e ''"
    if not bb.data.inherits_class('native', d):
        optional_quote = r"\(\"\?\)"
        s += " -e 's:${DEBUG_PREFIX_MAP}::g'"
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

BINCONFIG_GLOB ?= "*-config"

PACKAGE_PREPROCESS_FUNCS += "binconfig_package_preprocess"

binconfig_package_preprocess () {
	for config in `find ${PKGD} -type f -name '${BINCONFIG_GLOB}'`; do
		bbdebug 1 "Replacing paths in $config"
		sed -i \
		    -e 's:${DEBUG_PREFIX_MAP}::g;' \
		    -e 's:${TOOLCHAIN_OPTIONS}::g;' \
		    -e 's:${STAGING_BINDIR_CROSS}:${bindir}:g;' \
		    -e 's:${STAGING_BASELIBDIR}:${base_libdir}:g;' \
		    -e 's:${STAGING_LIBDIR}:${libdir}:g;' \
		    -e 's:${STAGING_INCDIR}:${includedir}:g;' \
		    -e 's:${STAGING_DATADIR}:${datadir}:g;' \
		    -e 's:${STAGING_DIR_HOST}${prefix}:${prefix}:g;' \
		    $config
	done
}

SYSROOT_PREPROCESS_FUNCS += "binconfig_sysroot_preprocess"

binconfig_sysroot_preprocess () {
	for config in `find ${D} -type f -name '${BINCONFIG_GLOB}'`; do
		bbdebug 1 "Replacing paths in $config"
		install -d ${SYSROOT_DESTDIR}${bindir_crossscripts}
		configname=`basename $config`
		newconfig=${SYSROOT_DESTDIR}${bindir_crossscripts}/$configname
		sed ${@get_binconfig_mangle(d)} $config > $newconfig.temp
		mv -f $newconfig.temp $newconfig
		chmod +x $newconfig
	done
}
