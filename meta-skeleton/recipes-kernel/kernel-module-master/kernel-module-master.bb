SUMMARY = "External kernel module dependency exemple - master module"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=1c5a04927650c42822bb4b1de4641658"

inherit module

PN = "kernel-module-master"
PV = "0.1"

SRC_URI = "file://Makefile \
           file://master.c \
           file://include/master.h \
           file://COPYING \
          "

S = "${WORKDIR}"

do_install_append() {
    install -Dm0644 ${S}/include/master.h ${D}${includedir}/${BPN}/
}
