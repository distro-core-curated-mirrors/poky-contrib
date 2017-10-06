LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

RPROVIDES_${PN} += "virtual/grub-bootconf"

inherit allarch

S = "${WORKDIR}"

GRUB_CFG = "${S}/grub-bootconf"
LABELS = "boot install"

ROOT = "root=PARTUUID=${DISK_SIGNATURE_UUID}"

python do_configure() {
    bb.build.exec_func('build_efi_cfg', d)
}

do_install() {
	install -d ${D}/boot
	install -d ${D}/boot/EFI
	install -d ${D}/boot/EFI/BOOT
	install -m 0744 grub-bootconf ${D}/boot/EFI/BOOT/grub.cfg
}

FILES_${PN} = "/boot/EFI/BOOT/grub.cfg"

inherit grub-efi-cfg
