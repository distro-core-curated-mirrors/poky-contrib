require ${COREBASE}/meta/recipes-core/images/core-image-minimal.bb

SUMMARY = "An image to use bmaptool to install core-image-minimal"
DESCRIPTION = "${SUMMARY}"

WKS_FILE = "image-bmap-installer.wks.in"
WKS_FILES = "${WKS_FILE}"

INITRD_IMAGE_LIVE = "core-image-bmap-installer-initramfs"

IMAGE_BOOT_FILES = "\
    core-image-minimal-${MACHINE}.wic;rootfs.img \
    core-image-minimal-${MACHINE}.wic.bmap;rootfs.img.bmap \
"

do_image_wic[depends] += "${INITRD_IMAGE_LIVE}:do_image_complete core-image-minimal:do_image_complete"

# If you are using meta-mender you only want a wic image created
# do_image_dataimg[noexec] = "1"
# do_image_mender[noexec] = "1"
# do_image_uefiimg[noexec] = "1"

inherit image

# We don't want to store our large image payload in sstate-cache
do_rootfs[nostamp] =  "1"
