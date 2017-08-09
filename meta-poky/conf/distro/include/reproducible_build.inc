
BUILD_REPRODUCIBLE_BINARIES = "1"

REPRODUCIBLE_TIMESTAMP_ROOTFS ?= "1483228802"

LDCONFIGDEPEND = ""

do_image_cpio[depends] += "cpio-replacement-native:do_populate_sysroot"
EXTRANATIVEPATH += "cpio-native"
IMAGE_CMD_CPIO = "cpio --ignore-devno --reproducible "

IMAGE_CMD_TAR = "tar -v --sort=name "

INHERIT += "reproducible_build"

