require recipes-kernel/linux/linux-yocto.inc

KBRANCH = "standard/preempt-rt/base"
KBRANCH_qemuppc = "standard/preempt-rt/qemuppc"

<<<<<<< HEAD
LINUX_VERSION ?= "3.4.59"
=======
LINUX_VERSION ?= "3.4.11"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
LINUX_KERNEL_TYPE = "preempt-rt"

KMETA = "meta"

<<<<<<< HEAD
SRCREV_machine ?= "2c997de11fbd934bdfe407b7f529b6561a476ea2"
SRCREV_machine_qemuppc ?= "3d2eb9c9a5c0c0b0048f687b3666b42cca26c7f2"
SRCREV_meta ?= "f36797c2df3fbe9491c8ac5977fb691f4a75e9b7"

PR = "${INC_PR}.1"
PV = "${LINUX_VERSION}+git${SRCPV}"

SRC_URI = "git://git.yoctoproject.org/linux-yocto-3.4.git;bareclone=1;branch=${KBRANCH},meta;name=machine,meta"
=======
SRCREV_machine ?= "5705c8037d2c47938034ead87c70ae3ebef552f7"
SRCREV_machine_qemuppc ?= "c8b651aab5d2d5c0839cdedc0c0ec5dc09cf47c0"
SRCREV_meta ?= "a201268353c030d9fafe00f2041976f7437d9386"

PR = "${INC_PR}.0"
PV = "${LINUX_VERSION}+git${SRCPV}"

SRC_URI = "git://git.yoctoproject.org/linux-yocto-3.4.git;protocol=git;bareclone=1;branch=${KBRANCH},meta;name=machine,meta"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

# Omit broken machines from COMPATIBLE_MACHINE
#   qemuppc hangs at boot
#   qemumips panics at boot
COMPATIBLE_MACHINE = "(qemux86|qemux86-64|qemuarm)"

# Functionality flags
<<<<<<< HEAD
KERNEL_FEATURES_append = " features/netfilter/netfilter.scc"
KERNEL_FEATURES_append = " features/taskstats/taskstats.scc"
KERNEL_FEATURES_append_qemux86 = " cfg/sound.scc"
KERNEL_FEATURES_append_qemux86-64 = " cfg/sound.scc"
KERNEL_FEATURES_append = " ${@bb.utils.contains("TUNE_FEATURES", "mx32", " cfg/x32.scc", "" ,d)}"
=======
KERNEL_FEATURES_append = " features/netfilter"
KERNEL_FEATURES_append = " features/taskstats"
KERNEL_FEATURES_append_qemux86 = " cfg/sound"
KERNEL_FEATURES_append_qemux86-64 = " cfg/sound"
KERNEL_FEATURES_append = " ${@bb.utils.contains("TUNE_FEATURES", "mx32", " cfg/x32", "" ,d)}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
