#
# Class to place yocto-kernel-cache fragments
# selections usfull to anyone
#

if bb.data.inherits_class('kernel-yacto', d):
    bb.warn("kernel-features class being inherited withou kernel-yacto")

KERNEL_FEATURES_append = " ${@bb.utils.contains("DISTRO_FEATURES", "apparmor", " features/apparmor/apparmor.scc", "" ,d)}"
KERNEL_FEATURES_append = " ${@bb.utils.contains("DISTRO_FEATURES", "smack", " features/smack/smack.scc", "" ,d)}"
KERNEL_FEATURES_append = " ${@bb.utils.contains("DISTRO_FEATURES", "dm-verity", " features/device-mapper/dm-verity.scc", "" ,d)}"
KERNEL_FEATURES_append = " ${@bb.utils.contains_any("MACHINE_FEATURES", "tpm tpm2", " features/tpm/tpm.scc","", d)}"
