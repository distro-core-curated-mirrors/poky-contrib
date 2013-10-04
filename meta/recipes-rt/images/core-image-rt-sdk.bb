require recipes-core/images/core-image-minimal.bb

DESCRIPTION = "Small image capable of booting a device with a test suite and \
tools for real-time use. It includes the full meta-toolchain, development \
headers and libraries to form a standalone SDK."
DEPENDS = "linux-yocto-rt"

<<<<<<< HEAD
IMAGE_FEATURES += "dev-pkgs tools-sdk tools-debug eclipse-debug tools-profile tools-testapps debug-tweaks"
=======
IMAGE_FEATURES += "dev-pkgs tools-sdk tools-debug tools-profile tools-testapps debug-tweaks"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

IMAGE_INSTALL += "rt-tests hwlatdetect kernel-dev"

LICENSE = "MIT"
