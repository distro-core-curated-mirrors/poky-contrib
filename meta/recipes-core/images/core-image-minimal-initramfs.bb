# Simple initramfs image. Mostly used for live images.
DESCRIPTION = "Small image capable of booting a device. The kernel includes \
the Minimal RAM-based Initial Root Filesystem (initramfs), which finds the \
<<<<<<< HEAD
first 'init' program more efficiently."
=======
first “init” program more efficiently."
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

IMAGE_INSTALL = "initramfs-live-boot initramfs-live-install initramfs-live-install-efi busybox udev base-passwd"

# Do not pollute the initrd image with rootfs features
IMAGE_FEATURES = ""

export IMAGE_BASENAME = "core-image-minimal-initramfs"
IMAGE_LINGUAS = ""

LICENSE = "MIT"

IMAGE_FSTYPES = "${INITRAMFS_FSTYPES}"
inherit core-image

IMAGE_ROOTFS_SIZE = "8192"
<<<<<<< HEAD

BAD_RECOMMENDATIONS += "busybox-syslog"
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
