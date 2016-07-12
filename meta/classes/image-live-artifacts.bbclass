# Copyright (C) 2004, Advanced Micro Devices, Inc.  All Rights Reserved
# Released under the MIT license (see packages/COPYING)

# Creates a bootable image using syslinux, your kernel and an optional
# initrd

#
# End result is two things:
#
# 1. A .hddimg file which is an msdos filesystem containing syslinux, a kernel,
# an initrd and a rootfs image. These can be written to harddisks directly and
# also booted on USB flash disks (write them there with dd).
#
# 2. A CD .iso image

# Boot process is that the initrd will boot and process which label was selected
# in syslinux. Actions based on the label are then performed (e.g. installing to
# an hdd)

# External variables (also used by syslinux.bbclass)
# ${INITRD} - indicates a list of filesystem images to concatenate and use as an initrd (optional)
# ${COMPRESSISO} - Transparent compress ISO, reduce size ~40% if set to 1
# ${NOISO}  - skip building the ISO image if set to 1
# ${NOHDD}  - skip building the HDD image if set to 1
# ${HDDIMG_ID} - FAT image volume-id
# ${ROOTFS} - indicates a filesystem image to include as the root filesystem (optional)

inherit live-vm-common

do_bootimg[depends] += "dosfstools-native:do_populate_sysroot \
                        mtools-native:do_populate_sysroot \
                        cdrtools-native:do_populate_sysroot \
                        virtual/kernel:do_deploy \
                        ${MLPREFIX}syslinux:do_populate_sysroot \
                        syslinux-native:do_populate_sysroot \
                        ${@oe.utils.ifelse(d.getVar('COMPRESSISO', False),'zisofs-tools-native:do_populate_sysroot','')} \
                        "


LABELS_LIVE ?= "boot install"

ARTIFACTS_DIR = "${DEPLOY_DIR_IMAGE}/artifacts"

populate_bootloader() {
	populate_kernel ${ARTIFACTS_DIR}

	if [ "${PCBIOS}" = "1" ]; then
		syslinux_hddimg_populate ${ARTIFACTS_DIR}
	fi
	if [ "${EFI}" = "1" ]; then
		efi_hddimg_populate ${ARTIFACTS_DIR}
	fi
}

python do_bootimg() {
    set_live_vm_vars(d, 'LIVE')
    if d.getVar("PCBIOS", True) == "1":
        bb.build.exec_func('build_syslinux_cfg', d)
    if d.getVar("EFI", True) == "1":
        bb.build.exec_func('build_efi_cfg', d)
    bb.build.exec_func('populate_bootloader', d)
}

addtask bootimg before do_image_complete
