SRC_URI = "git://git.seabios.org/seabios.git \
           file://seabios-e763ac3409893a2678debf1399e432a97268e577.patch \
           "
S = "${WORKDIR}/git"

DEPENDS = "acpica-native"

COMPATIBLE_MACHINE = "qemux86|qemux86-64"

PACKAGE_ARCH = "${MACHINE_ARCH}"

PV = "0.0+git${SRCPV}"
SRCREV = "b62632a3c78e39b9d5fbbed23779c12bac2c0f6b"
#SRCREV = "${AUTOREV}"

LICENSE = "GPLv3.0 & LGPLv3"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504 \
                    file://COPYING.LESSER;md5=6a6a8e020838b23406c81b19c1d46df6 \
                   "

CPPFLAGS[unexport] = "1"
CPP = "${TARGET_PREFIX}cpp"
export CROSS_PREFIX = "${TARGET_PREFIX}"

FILES_${PN} += "${datadir}/qemu/"

do_configure () {
	echo "CONFIG_CSM=y" > ${S}/.config
	echo "CONFIG_QEMU_HARDWARE=y" >> ${S}/.config
	yes '' | make oldconfig
	echo "CONFIG_QEMU=y" > ${S}/.config-vga
	echo "CONFIG_VGA_CIRRUS=y" >> ${S}/.config-vga
	yes '' | make KCONFIG_CONFIG=${S}/.config-vga OUT=out-vga/ oldconfig
}

do_compile () {
	oe_runmake
	oe_runmake KCONFIG_CONFIG=${S}/.config-vga OUT=out-vga/
}

do_install () {
	install -d ${D}${datadir}/seabios
	install ${S}/out/Csm16.bin ${D}${datadir}/seabios/
	install ${S}/out-vga/vgabios.bin ${D}${datadir}/seabios/
	#install -d ${D}${datadir}/qemu
	#install ${S}/out-vga/vgabios.bin ${D}${datadir}/qemu/vgabios-cirrus.bin
}