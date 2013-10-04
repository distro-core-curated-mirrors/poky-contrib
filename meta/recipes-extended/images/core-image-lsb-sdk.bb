<<<<<<< HEAD
require core-image-lsb.bb

=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
DESCRIPTION = "Basic image without X support suitable for Linux Standard Base \
(LSB) implementations. It includes the full meta-toolchain, plus development \
headers and libraries to form a standalone SDK."

<<<<<<< HEAD
IMAGE_FEATURES += "tools-sdk dev-pkgs tools-debug eclipse-debug tools-profile tools-testapps debug-tweaks"

IMAGE_INSTALL += "kernel-dev"

=======
IMAGE_FEATURES += "splash tools-sdk dev-pkgs ssh-server-openssh \
	tools-debug tools-profile tools-testapps debug-tweaks"


IMAGE_INSTALL = "\
    ${CORE_IMAGE_BASE_INSTALL} \
    packagegroup-core-basic \
    packagegroup-core-lsb \
    kernel-dev \
    "

inherit core-image
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
