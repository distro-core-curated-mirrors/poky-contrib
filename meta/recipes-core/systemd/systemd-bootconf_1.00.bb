LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

RPROVIDES_${PN} += "virtual/systemd-bootconf"

inherit allarch

S = "${WORKDIR}"

LABELS = "boot"

APPEND_append = " root=PARTUUID=${DISK_SIGNATURE_UUID}"

do_configure[vardeps] += "APPEND LABELS"

python do_configure() {
    bb.build.exec_func('build_efi_cfg', d)
}

do_install() {
	install -d ${D}/boot
	install -d ${D}/boot/loader
	install -d ${D}/boot/loader/entries
	install -m 0744 loader.conf ${D}/boot/loader/
        rm loader.conf
        install -m 077 *.conf ${D}/boot/loader/entries/
}

FILES_${PN} = "/boot/loader/* /boot/loader/entries/*"

inherit systemd-boot-cfg
