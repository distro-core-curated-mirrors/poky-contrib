DESCRIPTION = "Free and Open On-Chip Debugging, In-System Programming and Boundary-Scan Testing"
HOMEPAGE = "http://openocd.sourceforge.net"
LICENSE = "GPLv2 & BSD"
LIC_FILES_CHKSUM = "file://COPYING;md5=52aad3ae14f33671f4d848e9579f7870 \
                    file://jimtcl/LICENSE;md5=670d6aae00a2c7a4da40f70b78bdf992"
inherit autotools

SRC_URI = "http://sourceforge.net/projects/${BPN}/files/${BPN}/${PV}/${BP}.tar.bz2 \
           file://fix-jimtcl-configure.patch \
          "

SRC_URI[md5sum] = "8977a26a4e3a529e1c4fcc0df587a6a4"
SRC_URI[sha256sum] = "52237b786530c8460b221556c26fa4779f668b7dcb83ff14b8c5eb2050f38e63"

DEPENDS = "libftdi"
EXTRA_OECONF = " --enable-ft2232_libftdi --disable-ftdi2232 --disable-ftd2xx --enable-parport-ppdev"

BBCLASSEXTEND = "native"

