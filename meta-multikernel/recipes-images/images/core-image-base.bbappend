# Add tiny-linux to base image so we get two kernels
# One will be the "preferred_provider"
# the other will be "tiny-linux" as declared in
# linux-yocto-tiny_4.9.bbappend 
# with KERNEL_PACKAGE_NAME = "tiny-linux"
CORE_IMAGE_BASE_INSTALL += "tiny-linux"
