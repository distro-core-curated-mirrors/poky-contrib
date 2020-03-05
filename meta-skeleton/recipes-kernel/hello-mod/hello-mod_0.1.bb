SUMMARY = "Example of how to build an external Linux kernel module"
DESCRIPTION = "${SUMMARY}"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=12f884d2ae1ff87c09e5b7ccc2c4ca7e"

inherit module

# test 1: let the headers install from the shared kernel dir
#         From a kernel that doesn't inherit alt-headers
#         the headers will be in $WORKDIR/usr/alt
# inherit kernel-alt-headers
#
# test 2: depend on a kernel that is providing alt-headers
#         when it works, you'll have headers in:
#            recipe-sysroot/usr/alt-headers
DEPENDS += "virtual/kernel"

SRC_URI = "file://Makefile \
           file://hello.c \
           file://COPYING \
          "

S = "${WORKDIR}"

# The inherit of module.bbclass will automatically name module packages with
# "kernel-module-" prefix as required by the oe-core build environment.

RPROVIDES_${PN} += "kernel-module-hello"
