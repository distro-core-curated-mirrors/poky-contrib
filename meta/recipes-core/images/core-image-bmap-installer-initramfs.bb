require ${COREBASE}/meta/recipes-core/images/core-image-minimal-initramfs.bb

export IMAGE_BASENAME = "${MLPREFIX}core-image-bmap-installer-initramfs"

# We overwrite install-efi.sh
INITRAMFS_SCRIPTS:remove = "\
    initramfs-module-install-efi \
"

# Add our own install-efi.sh to avoid having to write a new wic plugin or changing grub-efi-cfg.bbclass
INITRAMFS_SCRIPTS:append = "\
    initramfs-module-install-bmap \
"
