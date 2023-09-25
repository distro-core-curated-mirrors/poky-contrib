SUMMARY = "A minimal container guest image"

require recipes-core/images/core-image-minimal.bb

IMAGE_LINGUAS = " "

IMAGE_ROOTFS_EXTRA_SPACE:append = "${@bb.utils.contains("DISTRO_FEATURES", "systemd", " + 40960", "" ,d)}"

