KBRANCH ?= "standard/base"

require recipes-kernel/linux/linux-yocto.inc

# board specific branches
KBRANCH_qemuarm  ?= "standard/arm-versatile-926ejs"
KBRANCH_qemuarm64 ?= "standard/qemuarm64"
KBRANCH_qemumips ?= "standard/mti-malta32"
KBRANCH_qemuppc  ?= "standard/qemuppc"
KBRANCH_qemux86  ?= "standard/base"
KBRANCH_qemux86-64 ?= "standard/base"
KBRANCH_qemumips64 ?= "standard/mti-malta64"

SRCREV_machine_qemuarm ?= "6eb15caf072384f62a3de67778f4f1e4b377b9c3"
SRCREV_machine_qemuarm64 ?= "918fc2fbdf48e86748a3600a5e79d1abcd71b92e"
SRCREV_machine_qemumips ?= "35a5713a9ee50a3aee884fcb236db197e73c97b5"
SRCREV_machine_qemuppc ?= "918fc2fbdf48e86748a3600a5e79d1abcd71b92e"
SRCREV_machine_qemux86 ?= "918fc2fbdf48e86748a3600a5e79d1abcd71b92e"
SRCREV_machine_qemux86-64 ?= "918fc2fbdf48e86748a3600a5e79d1abcd71b92e"
SRCREV_machine_qemumips64 ?= "30680adb38d14e55bc27f81fd45abf554f5f4845"
SRCREV_machine ?= "918fc2fbdf48e86748a3600a5e79d1abcd71b92e"
SRCREV_meta ?= "6377a5aee64780ccf4e4927da9d879b8f5fc9d66"

SRC_URI = "git://git.yoctoproject.org/linux-yocto-4.12.git;name=machine;branch=${KBRANCH}; \
           git://git.yoctoproject.org/yocto-kernel-cache;type=kmeta;name=meta;branch=yocto-4.12;destsuffix=${KMETA}"

LINUX_VERSION ?= "4.12.7"

PV = "${LINUX_VERSION}+git${SRCPV}"

KMETA = "kernel-meta"
KCONF_BSP_AUDIT_LEVEL = "2"

KERNEL_DEVICETREE_qemuarm = "versatile-pb.dtb"

COMPATIBLE_MACHINE = "qemuarm|qemuarm64|qemux86|qemuppc|qemumips|qemumips64|qemux86-64"

# Functionality flags
KERNEL_EXTRA_FEATURES ?= "features/netfilter/netfilter.scc"
KERNEL_FEATURES_append = " ${KERNEL_EXTRA_FEATURES}"
KERNEL_FEATURES_append_qemuall=" cfg/virtio.scc"
KERNEL_FEATURES_append_qemux86=" cfg/sound.scc cfg/paravirt_kvm.scc"
KERNEL_FEATURES_append_qemux86-64=" cfg/sound.scc cfg/paravirt_kvm.scc"
KERNEL_FEATURES_append = " ${@bb.utils.contains("TUNE_FEATURES", "mx32", " cfg/x32.scc", "" ,d)}"
