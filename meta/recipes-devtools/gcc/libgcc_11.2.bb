require recipes-devtools/gcc/gcc-${PV}.inc
require libgcc.inc

# Building with thumb enabled on armv6t fails
ARM_INSTRUCTION_SET:armv6 = "arm"

BBCLASSEXTEND += "mcextend:arm-none-eabi"

TARGET_ARCH:virtclass-mcextend-arm-none-eabi = "arm"
TARGET_VENDOR:virtclass-mcextend-arm-none-eabi = "-none"
TARGET_OS:virtclass-mcextend-arm-none-eabi = "eabi"

# Need to figure out how to produce for all arm architectures like debian packages/arm toolchain do 
TUNE_CCARGS:virtclass-mcextend-arm-none-eabi = " -mthumb -mfpu=neon -mfloat-abi=hard -mcpu=cortex-a15"

#HOST_ARCH:virtclass-mcextend-arm-none-eabi = "${TUNE_ARCH}"
#HOST_VENDOR:virtclass-mcextend-arm-none-eabi = "-poky"
#HOST_OS:virtclass-mcextend-arm-none-eabi = "linux${LIBCEXTENSION}${ABIEXTENSION}"
#HOST_PREFIX:virtclass-mcextend-arm-none-eabi = "${HOST_SYS}-"

do_configure:prepend:virtclass-mcextend-arm-none-eabi () {
        install -d ${STAGING_INCDIR}
        echo "" > ${STAGING_INCDIR}/limits.h
        sed -i -e 's#INHIBIT_LIBC_CFLAGS =.*#INHIBIT_LIBC_CFLAGS = -Dinhibit_libc#' ${B}/gcc/libgcc.mvars
        sed -i -e 's#inhibit_libc = false#inhibit_libc = true#' ${B}/gcc/Makefile
}

do_configure:append:virtclass-mcextend-arm-none-eabi () {
        sed -i -e 's#thread_header = .*#thread_header = gthr-single.h#' ${B}/${BPN}/Makefile
}

FILES:${PN}:virtclass-mcextend-arm-none-eabi = "${libdir}/arm*"
FILES:${PN}-dev:virtclass-mcextend-arm-none-eabi = "${libdir}/gcc"
FILES:${PN}-staticdev:virtclass-mcextend-arm-none-eabi = "${libdir}/gcc/*/*/*.a"

do_install:virtclass-mcextend-arm-none-eabi () {
        cd ${B}/${BPN}
        oe_runmake 'DESTDIR=${D}' MULTIBUILDTOP=${B}/${TARGET_SYS}/${BPN}/ install
}
