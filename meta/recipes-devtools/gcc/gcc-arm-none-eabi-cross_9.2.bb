TARGET_ARCH = "arm-none-eabi"
TARGET_OS = "none"
TARGET_VENDOR = ""
TARGET_SYS = "${TARGET_ARCH}"
TARGET_PREFIX = "${TARGET_SYS}-"
TARGET_CC_ARCH = ""
TARGET_LD_ARCH = ""
TARGET_AS_ARCH = ""

require recipes-devtools/gcc/gcc-${PV}.inc
require recipes-devtools/gcc/gcc-cross.inc

