require recipes-kernel/linux/linux-yocto.inc

KBRANCH_DEFAULT = "standard/base"
KBRANCH = "${KBRANCH_DEFAULT}"

<<<<<<< HEAD
SRCREV_machine_qemuarm ?= "e1dd6f40b76b3e9bd0686629004621aeddc6a982"
SRCREV_machine_qemumips  ?= "47af1ab871c8dfa4428cec26ec74e96a5b10c566"
SRCREV_machine_qemuppc ?= "65e4b20a87b02cf7bcb3ad3f725a079933828d4d"
SRCREV_machine_qemux86 ?= "ea977edd05ae2ebfa82731e0bee309bdfd08abee"
SRCREV_machine_qemux86-64 ?= "ea977edd05ae2ebfa82731e0bee309bdfd08abee"
SRCREV_machine ?= "ea977edd05ae2ebfa82731e0bee309bdfd08abee"
SRCREV_meta ?= "f36797c2df3fbe9491c8ac5977fb691f4a75e9b7"

SRC_URI = "git://git.yoctoproject.org/linux-yocto-3.4.git;bareclone=1;branch=${KBRANCH},${KMETA};name=machine,meta"

LINUX_VERSION ?= "3.4.59"

PR = "${INC_PR}.5"
=======
SRCREV_machine_qemuarm ?= "8ee53c3b82ada3cdfd7d25f07d3975834ac9a9b2"
SRCREV_machine_qemumips  ?= "caf99a20e3c3ba036ed1bb46875059a0d24e4fbd"
SRCREV_machine_qemuppc ?= "7833f1549c3d44cce8aea38b65cd501229aad492"
SRCREV_machine_qemux86 ?= "449f7f520350700858f21a5554b81cc8ad23267d"
SRCREV_machine_qemux86-64 ?= "449f7f520350700858f21a5554b81cc8ad23267d"
SRCREV_machine ?= "449f7f520350700858f21a5554b81cc8ad23267d"
SRCREV_meta ?= "a201268353c030d9fafe00f2041976f7437d9386"

SRC_URI = "git://git.yoctoproject.org/linux-yocto-3.4.git;protocol=git;nocheckout=1;branch=${KBRANCH},meta;name=machine,meta"

LINUX_VERSION ?= "3.4.11"

PR = "${INC_PR}.3"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
PV = "${LINUX_VERSION}+git${SRCPV}"

KMETA = "meta"

COMPATIBLE_MACHINE = "qemuarm|qemux86|qemuppc|qemumips|qemux86-64"

# Functionality flags
<<<<<<< HEAD
KERNEL_EXTRA_FEATURES ?= "features/netfilter/netfilter.scc"
KERNEL_FEATURES_append = " ${KERNEL_EXTRA_FEATURES}"
KERNEL_FEATURES_append_qemux86=" cfg/sound.scc cfg/paravirt_kvm.scc"
KERNEL_FEATURES_append_qemux86-64=" cfg/sound.scc"
KERNEL_FEATURES_append = " ${@bb.utils.contains("TUNE_FEATURES", "mx32", " cfg/x32.scc", "" ,d)}"
=======
KERNEL_REVISION_CHECKING=""
KERNEL_FEATURES_append = " features/netfilter"
KERNEL_FEATURES_append_qemux86=" cfg/sound"
KERNEL_FEATURES_append_qemux86-64=" cfg/sound"
KERNEL_FEATURES_append_qemux86=" cfg/paravirt_kvm"
KERNEL_FEATURES_append_qemux86-64=" cfg/paravirt_kvm"
KERNEL_FEATURES_append = " ${@bb.utils.contains("TUNE_FEATURES", "mx32", " cfg/x32", "" ,d)}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
