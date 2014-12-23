require binutils.inc
require binutils-${PV}.inc
require binutils-cross.inc

DEPENDS += "flex bison zlib"
PROVIDES = "virtual/binutils-target-avr"

BPN = "binutils"



python () {
    def replace(var, x, y):
        d.setVar(var, d.getVar(var, True).replace(d.expand(x),y))

    replace('CONFIGUREOPTS', '--target=${TARGET_SYS}','--target=avr')
    replace('EXTRA_OECONF', '--program-prefix=${TARGET_PREFIX}' ,'--program-prefix=avr-')
    replace('do_install', '${TARGET_PREFIX}' ,'avr-')
    replace('do_install', '${TARGET_SYS}' ,'avr')
}

EXTRA_OECONF += "--with-sysroot=/ \
                --enable-install-libbfd \
                --enable-install-libiberty \
                --enable-shared \
                "

do_install () {
    oe_runmake 'DESTDIR=${D}' install
}

sysroot_stage_all() {
    sysroot_stage_dirs ${D} ${SYSROOT_DESTDIR}
    sysroot_stage_dir ${D}${STAGING_DIR_NATIVE}${prefix_native}/avr ${SYSROOT_DESTDIR}${STAGING_DIR_NATIVE}${prefix_native}/avr
    sysroot_stage_dir ${D}${STAGING_DIR_NATIVE}${prefix_native}/${BUILD_SYS} ${SYSROOT_DESTDIR}${STAGING_DIR_NATIVE}${prefix_native}/${BUILD_SYS}
}

