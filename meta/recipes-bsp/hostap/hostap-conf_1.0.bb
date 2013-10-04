DESCRIPTION = "PCMCIA-cs configuration files for wireless LAN cards based on Intersil's Prism2/2.5/3 chipset"
SECTION = "kernel/modules"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=393a5ca445f6965873eca0259a17f833"
<<<<<<< HEAD
PR = "r15"
=======
RDEPENDS_${PN} = "update-modules"
PR = "r14"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

SRC_URI = "file://hostap_cs.modalias \
           file://COPYING.patch"

inherit allarch

do_compile() {
}

do_install() {
	install -d ${D}${sysconfdir}/modprobe.d

	install -m 0644 ${WORKDIR}/hostap_cs.modalias ${D}${sysconfdir}/modprobe.d/hostap_cs.conf
}

