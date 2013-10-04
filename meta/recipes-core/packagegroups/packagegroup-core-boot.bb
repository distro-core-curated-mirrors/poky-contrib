#
# Copyright (C) 2007 OpenedHand Ltd.
#

SUMMARY = "Minimal boot requirements"
DESCRIPTION = "The minimal set of packages required to boot the system"
LICENSE = "MIT"
DEPENDS = "virtual/kernel"
<<<<<<< HEAD
PR = "r11"
=======
PR = "r10"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

inherit packagegroup

PACKAGE_ARCH = "${MACHINE_ARCH}"

#
# Set by the machine configuration with packages essential for device bootup
#
MACHINE_ESSENTIAL_EXTRA_RDEPENDS ?= ""
MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS ?= ""

# For backwards compatibility after rename
RPROVIDES_${PN} = "task-core-boot"
RREPLACES_${PN} = "task-core-boot"
RCONFLICTS_${PN} = "task-core-boot"

# Distro can override the following VIRTUAL-RUNTIME providers:
VIRTUAL-RUNTIME_dev_manager ?= "udev"
<<<<<<< HEAD
VIRTUAL-RUNTIME_login_manager ?= "busybox"
=======
VIRTUAL-RUNTIME_login_manager ?= "tinylogin"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
VIRTUAL-RUNTIME_init_manager ?= "sysvinit"
VIRTUAL-RUNTIME_initscripts ?= "initscripts"
VIRTUAL-RUNTIME_keymaps ?= "keymaps"

<<<<<<< HEAD
SYSVINIT_SCRIPTS = "${@base_contains('MACHINE_FEATURES', 'rtc', 'busybox-hwclock', '', d)} \
                    modutils-initscripts \
                    init-ifupdown \
                   "

=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
RDEPENDS_${PN} = "\
    base-files \
    base-passwd \
    busybox \
<<<<<<< HEAD
    ${@base_contains("DISTRO_FEATURES", "sysvinit", "${SYSVINIT_SCRIPTS}", "", d)} \
    ${@base_contains("MACHINE_FEATURES", "keyboard", "${VIRTUAL-RUNTIME_keymaps}", "", d)} \
    netbase \
    ${VIRTUAL-RUNTIME_login_manager} \
    ${VIRTUAL-RUNTIME_init_manager} \
    ${VIRTUAL-RUNTIME_initscripts} \
=======
    ${@base_contains("MACHINE_FEATURES", "rtc", "busybox-hwclock", "", d)} \
    ${VIRTUAL-RUNTIME_initscripts} \
    ${@base_contains("MACHINE_FEATURES", "keyboard", "${VIRTUAL-RUNTIME_keymaps}", "", d)} \
    modutils-initscripts \
    netbase \
    ${VIRTUAL-RUNTIME_login_manager} \
    ${VIRTUAL-RUNTIME_init_manager} \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    ${VIRTUAL-RUNTIME_dev_manager} \
    ${VIRTUAL-RUNTIME_update-alternatives} \
    ${MACHINE_ESSENTIAL_EXTRA_RDEPENDS}"

RRECOMMENDS_${PN} = "\
    ${MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS}"
