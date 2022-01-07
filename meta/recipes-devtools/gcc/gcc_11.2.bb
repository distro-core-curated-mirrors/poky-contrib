require recipes-devtools/gcc/gcc-${PV}.inc
require gcc-target.inc

# Building with thumb enabled on armv4t armv5t fails with
# | gcc-4.8.1-r0/gcc-4.8.1/gcc/cp/decl.c:7438:(.text.unlikely+0x2fa): relocation truncated to fit: R_ARM_THM_CALL against symbol `fancy_abort(char const*, int, char const*)' defined in .glue_7 section in linker stubs
# | gcc-4.8.1-r0/gcc-4.8.1/gcc/cp/decl.c:7442:(.text.unlikely+0x318): additional relocation overflows omitted from the output
ARM_INSTRUCTION_SET:armv4 = "arm"
ARM_INSTRUCTION_SET:armv5 = "arm"

ARMFPARCHEXT:armv6 = "${@'+fp' if d.getVar('TARGET_FPU') == 'hard' else ''}"
ARMFPARCHEXT:armv7a = "${@'+fp' if d.getVar('TARGET_FPU') == 'hard' else ''}"
ARMFPARCHEXT:armv7ve = "${@'+fp' if d.getVar('TARGET_FPU') == 'hard' else ''}"

BBCLASSEXTEND = "nativesdk mcextend:arm-none-eabi"

TARGET_ARCH:virtclass-mcextend-arm-none-eabi = "arm"
TARGET_VENDOR:virtclass-mcextend-arm-none-eabi = "-none"
TARGET_OS:virtclass-mcextend-arm-none-eabi ="eabi"

HOST_ARCH:virtclass-mcextend-arm-none-eabi = "${TUNE_ARCH}"
HOST_VENDOR:virtclass-mcextend-arm-none-eabi = "-poky"
HOST_OS:virtclass-mcextend-arm-none-eabi ="linux${LIBCEXTENSION}${ABIEXTENSION}"
HOST_PREFIX:virtclass-mcextend-arm-none-eabi = "${HOST_SYS}-"

# gcc proper already has it set in global securty config
SECURITY_STRINGFORMAT:virtclass-mcextend-arm-none-eabi = ""

# Everything must be prefixed with ${PN} to avoid clashes with plain gcc
PACKAGES:virtclass-mcextend-arm-none-eabi = "\
    ${PN} ${PN}-plugins ${PN}-symlinks \
    ${PN}-g++ ${PN}-g++-symlinks \
    ${PN}-cpp ${PN}-cpp-symlinks \
    ${PN}-g77 ${PN}-g77-symlinks \
    ${PN}-gfortran ${PN}-gfortran-symlinks \
    ${PN}-gcov ${PN}-gcov-symlinks \
    ${PN}-doc \
    ${PN}-dev \
    ${PN}-dbg \
"

RDEPENDS:${PN}:virtclass-mcextend-arm-none-eabi = "${PN}-cpp"

FILES:${PN}-cpp = "\
    ${bindir}/${TARGET_PREFIX}cpp* \
    ${base_libdir}/cpp \
    ${libexecdir}/gcc/${TARGET_SYS}/${BINV}/cc1"
FILES:${PN}-cpp-symlinks = "${bindir}/cpp"

FILES:${PN}-gcov = "${bindir}/${TARGET_PREFIX}gcov* \
    ${bindir}/${TARGET_PREFIX}gcov-tool* \
"
FILES:${PN}-gcov-symlinks = "${bindir}/gcov \
    ${bindir}/gcov-tool \
"

FILES:${PN}-g++ = "\
    ${bindir}/${TARGET_PREFIX}g++* \
    ${libexecdir}/gcc/${TARGET_SYS}/${BINV}/cc1plus \
"
FILES:${PN}-g++-symlinks = "\
    ${bindir}/c++ \
    ${bindir}/g++ \
"
