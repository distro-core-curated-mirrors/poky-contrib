require recipes-devtools/gcc/gcc-${PV}.inc
require gcc-cross.inc

BPN = "gcc"
PROVIDES = "virtual/gcc-target-avr"

ARCH_FLAGS_FOR_TARGET = ""
TARGET_CFLAGS = ""

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
                --enable-linker-build-id \
                --with-ppl=no \
                --with-cloog=no \
                --enable-checking=release \
                ${EXTRA_OECONF_PATHS}"

python () {
    def replace(var, x, y):
        #bb.warn(x)
        #bb.warn(d.expand(x))
        #bb.warn(d.getVar(var))
        #bb.warn(d.getVar(var, True).replace(d.expand(x),y))
        d.setVar(var, d.getVar(var, True).replace(d.expand(x),y))

    replace('CONFIGUREOPTS', '--target=${TARGET_SYS}','--target=avr')
    #replace('do_configure', '${HOST_PREFIX}' ,'avr-')
    replace('do_install', '${TARGET_PREFIX}' ,'avr-')
    replace('do_install', '${TARGET_SYS}' ,'avr')
}

