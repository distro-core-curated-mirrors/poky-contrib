
AUTO_SYSLINUXCFG = "1"
INITRD_IMAGE ?= "core-image-minimal-initramfs"
INITRD ?= "${DEPLOY_DIR_IMAGE}/${INITRD_IMAGE}-${MACHINE}.cpio.gz"
SYSLINUX_ROOT = "root=/dev/ram0 "
SYSLINUX_TIMEOUT ?= "10"
SYSLINUX_LABELS ?= "boot install"
LABELS_append = " ${SYSLINUX_LABELS} "

ROOTFS ?= "${DEPLOY_DIR_IMAGE}/${IMAGE_BASENAME}-${MACHINE}.ext3"

do_bootimg[depends] += "${INITRD_IMAGE}:do_rootfs"
<<<<<<< HEAD
do_bootimg[depends] += "${PN}:do_rootfs"
=======
do_bootimg[depends] += "${IMAGE_BASENAME}:do_rootfs"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

inherit bootimg
