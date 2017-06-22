LICENSE = "MIT"
inherit core-image
IMAGE_FEATURES += "ssh-server-openssh"
IMAGE_INSTALL += "docker docker-contrib"
IMAGE_INSTALL += "connman connman-client"

# Add 8GB to image
IMAGE_ROOTFS_EXTRA_SPACE = "8388608"

# Ensure we don't get FAT specific > 4GB size error
# IMAGE_FSTYPES_remove = "live"
NOHDD = "1"
NOISO = "1"
