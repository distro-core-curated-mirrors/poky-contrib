<<<<<<< HEAD
require core-image-lsb.bb

=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
DESCRIPTION = "Basic image without X support suitable for development work. It \
can be used for customization and implementations that conform to Linux \
Standard Base (LSB)."

<<<<<<< HEAD
IMAGE_FEATURES += "dev-pkgs"
=======
IMAGE_FEATURES += "splash dev-pkgs ssh-server-openssh"

IMAGE_INSTALL = "\
    ${CORE_IMAGE_BASE_INSTALL} \
    packagegroup-core-basic \
    packagegroup-core-lsb \
    "

inherit core-image
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
