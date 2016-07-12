# Create the artifacts only on an ARTIFACTS_DIR,
# which can be later picked up by wic

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

#python do_bootimg() {
#    set_live_vm_vars(d, 'LIVE')
#    if d.getVar("PCBIOS", True) == "1":
#        bb.build.exec_func('build_syslinux_cfg', d)
#    if d.getVar("EFI", True) == "1":
#        bb.build.exec_func('build_efi_cfg', d)
#    bb.build.exec_func('populate_bootloader', d)
#}

#addtask bootimg before do_image_complete
