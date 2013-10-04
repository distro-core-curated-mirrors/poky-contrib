require recipes-kernel/linux/linux-yocto.inc

# We need lzma (as CONFIG_KERNEL_LZMA=y)
DEPENDS += "xz-native"

KBRANCH_DEFAULT = "standard/tiny/base"
KBRANCH = "${KBRANCH_DEFAULT}"
LINUX_KERNEL_TYPE = "tiny"
KCONFIG_MODE = "--allnoconfig"

<<<<<<< HEAD
LINUX_VERSION ?= "3.4.59"

KMETA = "meta"

SRCREV_machine ?= "ea977edd05ae2ebfa82731e0bee309bdfd08abee"
SRCREV_meta ?= "f36797c2df3fbe9491c8ac5977fb691f4a75e9b7"

PR = "${INC_PR}.1"
PV = "${LINUX_VERSION}+git${SRCPV}"

SRC_URI = "git://git.yoctoproject.org/linux-yocto-3.4.git;bareclone=1;branch=${KBRANCH},meta;name=machine,meta"
=======
LINUX_VERSION ?= "3.4.11"

KMETA = "meta"

SRCREV_machine ?= "449f7f520350700858f21a5554b81cc8ad23267d"
SRCREV_meta ?= "a201268353c030d9fafe00f2041976f7437d9386"


PR = "${INC_PR}.0"
PV = "${LINUX_VERSION}+git${SRCPV}"

SRC_URI = "git://git.yoctoproject.org/linux-yocto-3.4;protocol=git;bareclone=1;branch=${KBRANCH},meta;name=machine,meta"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

COMPATIBLE_MACHINE = "(qemux86)"

# Functionality flags
KERNEL_FEATURES = ""
