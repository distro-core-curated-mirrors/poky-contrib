
SUMMARY = "useradd test A"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/LICENSE;md5=4d92cd373abda3937c2bc47fbc49d690 \
                    file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

ALLOW_EMPTY_${PN} = "1"
inherit allarch useradd
USERADD_PACKAGES = "${PN}"

GROUPADD_PARAM_${PN} = " --system testgroupa"
USERADD_PARAM_${PN} = "-N -g testgroupa testusera"
