KBRANCH_genericx86  = "standard/base"
KBRANCH_genericx86-64  = "standard/base"

KMACHINE_genericx86 ?= "common-pc"
KMACHINE_genericx86-64 ?= "common-pc-64"
KBRANCH_edgerouter = "standard/edgerouter"
KBRANCH_beaglebone = "standard/beaglebone"
KBRANCH_mpc8315e-rdb = "standard/fsl-mpc8315e-rdb"

SRCREV_machine_genericx86    ?= "4700f2f8b9dbaad5ae441b682d04b09e811135fc"
SRCREV_machine_genericx86-64 ?= "4700f2f8b9dbaad5ae441b682d04b09e811135fc"
SRCREV_machine_edgerouter ?= "c85c54f5bf53b98afe8105e91bffcdb6c60afe8f"
SRCREV_machine_beaglebone ?= "c85c54f5bf53b98afe8105e91bffcdb6c60afe8f"
SRCREV_machine_mpc8315e-rdb ?= "6b67f448d63917f5ea306eb293cd9844077e4a61"

COMPATIBLE_MACHINE_genericx86 = "genericx86"
COMPATIBLE_MACHINE_genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE_edgerouter = "edgerouter"
COMPATIBLE_MACHINE_beaglebone = "beaglebone"
COMPATIBLE_MACHINE_mpc8315e-rdb = "mpc8315e-rdb"

LINUX_VERSION_genericx86 = "4.9.6"
LINUX_VERSION_genericx86-64 = "4.9.6"
LINUX_VERSION_edgerouter = "4.9.8"
LINUX_VERSION_beaglebone = "4.9.8"
LINUX_VERSION_mpc8315e-rdb = "4.9.8"
FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
LINUX_VERSION_qemunios2 = "4.9.9"
COMPATIBLE_MACHINE_qemunios2 = "qemunios2"

# During some modules compilation we get some unresolved externals:
# __mulsi3, __lshrdi3, ...
# So we exclude these modules via using a modified defconfig.

SRC_URI_append_qemunios2 = " file://defconfig"
#KBUILD_DEFCONFIG_qemunios2 = "10m50_defconfig"
