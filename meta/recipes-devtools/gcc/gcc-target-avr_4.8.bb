require recipes-devtools/gcc/gcc-${PV}.inc
require gcc-target.inc

BPN = "gcc"

ARCH_FLAGS_FOR_TARGET = ""

EXTRA_OECONF = "${@['--enable-clocale=generic', ''][d.getVar('USE_NLS', True) != 'no']} \
                --with-gnu-ld \
                --enable-languages=c \
                ${GCCMULTILIB} \
                --disable-libssp \
                --program-prefix=avr- \
                --without-local-prefix \
                ${OPTSPACE} \
                --enable-lto \
                --disable-bootstrap \
                --disable-libmudflap \
                --with-system-zlib \
                --with-ppl=no \
                --with-cloog=no \
                --enable-checking=release \
                ${EXTRA_OECONF_PATHS}"


python () {
    def replace(var, x, y, d):
        d.setVar(var, d.getVar(var, True).replace(d.expand(x),y))

    ld = bb.data.createCopy(d)
    ld.setVar("TARGET_CFLAGS", "")
    ld.setVar("HOST_CC_ARCH", "")
    ld.setVar("TOOLCHAIN_OPTIONS", "")

    replace('CONFIGUREOPTS', '--target=${TARGET_SYS}','--target=avr', d)
    replace('EXTRA_OECONF', '--program-prefix=${TARGET_PREFIX}' ,'--program-prefix=avr-', d)
    replace('do_configure', '${HOST_PREFIX}' ,'avr-', ld)
    d.setVar('do_configure', ld.getVar('do_configure'))
    replace('do_install', '${TARGET_PREFIX}' ,'avr-', d)
    replace('do_install', '${TARGET_SYS}' ,'avr', d)
    replace(d.expand('FILES_${PN}'), '${TARGET_PREFIX}' ,'avr-', d)
    replace(d.expand('FILES_cpp'), '${TARGET_PREFIX}' ,'avr-', d)
    replace(d.expand('FILES_gcov'), '${TARGET_PREFIX}' ,'avr-', d)
    replace(d.expand('FILES_${PN}'), '${TARGET_SYS}' ,'avr', d)
    replace(d.expand('FILES_${PN}-plugin-dev'), '${TARGET_SYS}' ,'avr', d)
    replace(d.expand('FILES_${PN}-dbg'), '${TARGET_SYS}' ,'avr', d)
    replace(d.expand('FILES_${PN}-dev'), '${TARGET_SYS}' ,'avr', d)
    #d.appendVar(d.expand('FILES_${PN}'), " ${exec_prefix}/${HOST_SYS}/avr/lib/*-*.so")
    #d.appendVar(d.expand('FILES_${PN}-dbg'), " ${exec_prefix}/${HOST_SYS}/avr/lib/.debug")
}
