SUMMARY = "External kernel module dependency exemple - slave module"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=1c5a04927650c42822bb4b1de4641658"

inherit module

PN = "kernel-module-slave"
PV = "0.1"

DEPENDS = "kernel-module-master"

SRC_URI = "file://Makefile \
           file://slave.c \
           file://COPYING \
          "

S = "${WORKDIR}"
