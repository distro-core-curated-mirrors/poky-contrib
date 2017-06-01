# Simple initramfs image. Mostly used for live images.
DESCRIPTION = "Systemd-boot based EFI system"
LICENSE = "MIT"

inherit deploy
do_deploy() {
	bbwarn ${DEPLOYDIR}

	EFIDIR="EFI/BOOT"
	EFI_IMAGE="systemd-bootia32.efi"
	DEST_EFI_IMAGE="bootia32.efi"
	if [ "${TARGET_ARCH}" = "x86_64" ]; then
	    EFI_IMAGE="systemd-bootx64.efi"
	    DEST_EFI_IMAGE="bootx64.efi"
	fi

	install -d ${DEPLOY_DIR_IMAGE}/bootfs/${EFIDIR}
	# systemd-boot requires these paths for configuration files
	# they are not customizable so no point in new vars
	install -d ${DEPLOY_DIR_IMAGE}/bootfs/loader/entries
	install -m 0644 ${DEPLOY_DIR_IMAGE}/${EFI_IMAGE} ${DEPLOY_DIR_IMAGE}/bootfs/${EFIDIR}/${DEST_EFI_IMAGE}
	install -m 0644 ${DEPLOY_DIR_IMAGE}/${KERNEL_IMAGETYPE} ${DEPLOY_DIR_IMAGE}/bootfs/vmlinuz

}

do_deploy[depends] = "${MLPREFIX}systemd-boot:do_deploy virtual/kernel:do_deploy"
addtask do_deploy after do_prepare_recipe_sysroot before do_wic_image

# Use the same restriction as initramfs-live-install
COMPATIBLE_HOST = "(i.86|x86_64).*-linux"
