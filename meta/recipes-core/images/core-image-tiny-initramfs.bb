# Simple initramfs image artifact generation for tiny images.
DESCRIPTION = "Tiny image capable of booting a device. The kernel includes \
the Minimal RAM-based Initial Root Filesystem (initramfs), which finds the \
first 'init' program more efficiently. core-image-tiny-initramfs doesn't \
actually generate an image but rather generates boot and rootfs artifacts \
that can subsequently be picked up by external image generation tools such as wic."

PACKAGE_INSTALL = "initramfs-live-boot-tiny packagegroup-core-boot dropbear ${VIRTUAL-RUNTIME_base-utils} ${VIRTUAL-RUNTIME_dev_manager} base-passwd ${ROOTFS_BOOTSTRAP_INSTALL}"

# Do not pollute the initrd image with rootfs features
IMAGE_FEATURES = ""

export IMAGE_BASENAME = "core-image-tiny-initramfs"
IMAGE_LINGUAS = ""

LICENSE = "MIT"

# don't actually generate an image, just the artifacts needed for one
IMAGE_FSTYPES = "${INITRAMFS_FSTYPES}"

inherit core-image

IMAGE_ROOTFS_SIZE = "8192"
IMAGE_ROOTFS_EXTRA_SPACE = "0"

BAD_RECOMMENDATIONS += "busybox-syslog"

# Should be compatible with initramfs-live-install
COMPATIBLE_HOST = "(i.86|x86_64|arm).*-linux"

QB_KERNEL_CMDLINE_APPEND += "debugshell=3 init=/bin/busybox sh init"

# Avoid getting input from previously listed console tty
QB_KERNEL_CMDLINE_APPEND_append_arm  = " console=ttyAMA0,115200"
