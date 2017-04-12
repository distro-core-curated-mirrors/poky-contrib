DEPENDS += "useraddtest-a"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/LICENSE;md5=4d92cd373abda3937c2bc47fbc49d690 \
                    file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

FILES_${PN} = "${datadir}/foo"

DEPENDS += "shadow-native"

do_install () {
	   mkdir -p ${D}${datadir}
	   echo foo > ${D}${datadir}/foo
	   chown foo:foo ${D}${datadir}/foo
}
