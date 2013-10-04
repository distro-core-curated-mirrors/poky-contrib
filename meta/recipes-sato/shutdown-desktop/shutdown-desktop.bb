SUMMARY = "Provides an icon to shut down the system cleanly"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/LICENSE;md5=3f40d7994397109285ec7b81fdeb3b58 \
                    file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

SRC_URI = "file://shutdown.desktop"

PR = "r1"

S = "${WORKDIR}"

do_install() {
	install -d ${D}${datadir}/applications
	install -m 0644 shutdown.desktop ${D}${datadir}/applications/
<<<<<<< HEAD

	sed -i ${D}${datadir}/applications/shutdown.desktop -e 's#^Exec=\(.*\)#Exec=${base_sbindir}/\1#'
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
}

pkg_postinst_${PN} () {
    grep -q qemuarm $D${sysconfdir}/hostname && \
<<<<<<< HEAD
        sed -i $D${datadir}/applications/shutdown.desktop -e 's#^Exec=\(.*\)/halt#Exec=\1/reboot#' \
=======
        sed -i $D${datadir}/applications/shutdown.desktop -e 's/^Exec=halt/Exec=reboot/' \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        || true
}

inherit allarch
