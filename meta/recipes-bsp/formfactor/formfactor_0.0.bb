DESCRIPTION = "Device formfactor information"
SECTION = "base"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/LICENSE;md5=3f40d7994397109285ec7b81fdeb3b58 \
                    file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"
<<<<<<< HEAD
PR = "r41"
=======
PR = "r21"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

SRC_URI = "file://config file://machconfig"
S = "${WORKDIR}"

PACKAGE_ARCH = "${MACHINE_ARCH}"
INHIBIT_DEFAULT_DEPS = "1"

do_install() {
	# Only install file if it has a contents
        install -d ${D}${sysconfdir}/formfactor/
        install -m 0644 ${S}/config ${D}${sysconfdir}/formfactor/
	if [ -s "${S}/machconfig" ]; then
	        install -m 0644 ${S}/machconfig ${D}${sysconfdir}/formfactor/
	fi
}
