DESCRIPTION = "A console-only image with more full-featured Linux system \
functionality installed."

IMAGE_FEATURES += "splash ssh-server-openssh"

IMAGE_GITPW_INSTALL = "python-requests python-git"
IMAGE_PTOE_INSTALL = "python-pyparsing python-unidiff"


IMAGE_INSTALL = "\
    packagegroup-core-boot \
    packagegroup-core-full-cmdline \
    ${CORE_IMAGE_EXTRA_INSTALL} \
    git \
    python \
    python-modules \
    ${IMAGE_GITPW_INSTALL} \
    ${IMAGE_PTOE_INSTALL} \
    "

inherit core-image

