require binutils.inc
require binutils-${PV}.inc

DEPENDS += "flex bison zlib"

BPN = "binutils"

FILES_${PN}-dev += " \
    ${exec_prefix}/${HOST_SYS}/avr/lib/lib*.la \
    ${exec_prefix}/${HOST_SYS}/avr/lib/libopcodes.so \
    ${exec_prefix}/${HOST_SYS}/avr/lib/libbfd.so \
    ${exec_prefix}/${HOST_SYS}/avr/include \
"
FILES_${PN}-staticdev += " \
    ${exec_prefix}/${HOST_SYS}/avr/lib/lib*.a \
"

USE_ALTERNATIVES_FOR = ""

python () {
    def replace(var, x, y):
        d.setVar(var, d.getVar(var, True).replace(d.expand(x),y))

    replace('CONFIGUREOPTS', '--target=${TARGET_SYS}','--target=avr')
    replace('EXTRA_OECONF', '--program-prefix=${TARGET_PREFIX}' ,'--program-prefix=avr-')
    replace('do_install', '${TARGET_PREFIX}' ,'avr-')
    replace('do_install', '${TARGET_SYS}' ,'avr')
    replace(d.expand('FILES_${PN}'), '${TARGET_PREFIX}' ,'avr-')
    replace(d.expand('FILES_${PN}'), '${TARGET_SYS}' ,'avr')
    d.appendVar(d.expand('FILES_${PN}'), " ${exec_prefix}/${HOST_SYS}/avr/lib/*-*.so ${libdir}/ldscripts")
    d.appendVar(d.expand('FILES_${PN}-dbg'), " ${exec_prefix}/${HOST_SYS}/avr/lib/.debug")
}

EXTRA_OECONF += "--with-sysroot=/ \
                --enable-install-libbfd \
                --enable-install-libiberty \
                --enable-shared \
                "

#do_install_append() {
#	# Remove symlinks created by do_install
#	for p in ${TARGET_PREFIX}* ; do
#		rm `echo $p | sed -e s,${TARGET_PREFIX},,`
#	done
#}

do_install () {
    autotools_do_install

    # Fix the /usr/${TARGET_SYS}/bin/* links
    for l in ${D}${prefix}/${TARGET_SYS}/bin/*; do
	rm -f $l
	ln -sf `echo ${prefix}/${TARGET_SYS}/bin \
	    | tr -s / \
	    | sed -e 's,^/,,' -e 's,[^/]*,..,g'`${bindir}/${TARGET_PREFIX}`basename $l` $l
    done
}