SUMMARY = "Adds a user called yoctouser"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

inherit useradd
inherit allarch

USERADD_PACKAGES = "${PN}"

USERADD_PARAM_${PN} = "-d /home/yoctouser -m yoctouser"

ALLOW_EMPTY_${PN} = "1"
