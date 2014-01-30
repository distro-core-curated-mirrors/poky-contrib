DESCRIPTION = "Free and Open On-Chip Debugging, In-System Programming and Boundary-Scan Testing"
HOMEPAGE = "http://openocd.sourceforge.net"
LICENSE = "GPLv2 & BSD"
LIC_FILES_CHKSUM = "file://COPYING;md5=b234ee4d69f5fce4486a80fdaf4a4263 \
                    file://jimtcl/LICENSE;md5=670d6aae00a2c7a4da40f70b78bdf992"
inherit autotools

SRC_URI = "git://git.code.sf.net/p/openocd/code \
           file://fix-jimtcl-configure.patch \
           file://0001-quark_x10xx-add-new-target-quark_x10xx.patch \
          "

SRCREV = "bb8c0d55d4fa72fe48ef70f17ee40324a355b73f"

S = "${WORKDIR}/git"
PV = "0.7.0+git${SRCPV}"

do_submodule () {
	git submodule init
	git submodule update
}
addtask submodule after do_unpack before do_patch

SRC_URI[md5sum] = "8977a26a4e3a529e1c4fcc0df587a6a4"
SRC_URI[sha256sum] = "52237b786530c8460b221556c26fa4779f668b7dcb83ff14b8c5eb2050f38e63"

DEPENDS = "libftdi"
EXTRA_OECONF = " --enable-ft2232_libftdi --disable-ftdi2232 --disable-ftd2xx --enable-parport-ppdev"

BBCLASSEXTEND = "native"

