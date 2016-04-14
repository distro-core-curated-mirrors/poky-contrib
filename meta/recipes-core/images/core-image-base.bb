SUMMARY = "A console-only image that fully supports the target device \
hardware."

IMAGE_FEATURES += "splash  ssh-server-openssh"

LICENSE = "MIT"

inherit core-image

IMAGE_INSTALL += "strace forktest gdb prelink"

