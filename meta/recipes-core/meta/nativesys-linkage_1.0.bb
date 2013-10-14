DESCRIPTION = "Linkage/Setup for native system development machine"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/LICENSE;md5=3f40d7994397109285ec7b81fdeb3b58 \
                    file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

INHIBIT_DEFAULT_DEPS = "1"

do_install () {
	install -d ${D}/lib/ ${D}/usr/lib/
	ln -s /usr/lib/gcc ${D}/usr/lib/gcc
	ln -s ../ ${D}/lib/x86_64-linux-gnu
	ln -s ../ ${D}/usr/lib/x86_64-linux-gnu
}