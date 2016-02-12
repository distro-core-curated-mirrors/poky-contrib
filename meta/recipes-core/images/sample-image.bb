PACKAGE_INSTALL = "busybox coreutils grep bash yoctouser"
IMAGE_FEATURES = ""
IMAGE_LINGUAS = ""
USER_CLASSES = "image-mklibs"

IMAGE_FSTYPES = "tar.bz2"

LICENSE = "MIT"

INHIBIT_DEFAULT_DEPS = "1"

inherit image
