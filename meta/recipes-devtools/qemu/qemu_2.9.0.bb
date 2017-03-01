require qemu.inc

LIC_FILES_CHKSUM = "file://COPYING;md5=441c28d2cf86e15a37fa47e15a72fbac \
                    file://COPYING.LIB;endline=24;md5=c04def7ae38850e7d3ef548588159913"

#SRCREV="685783c5b69c83c942d1fc21679311eeb8f79ab9"
SRCREV="ad584d37f2a86b392c25f3f00cc1f1532676c2d1"
SRC_URI += "git://github.com/qemu/qemu.git;protocol=https"

SRC_URI[md5sum] = "17940dce063b6ce450a12e719a6c9c43"
SRC_URI[sha256sum] = "dafd5d7f649907b6b617b822692f4c82e60cf29bc0fc58bc2036219b591e5e62"
SRC_URI += "file://0001-nios2-Add-Altera-JTAG-UART-emulation.patch \
            file://0002-altera_10m_50-New-devices.patch \
            file://0001-FIXME-nios2-Altera-TSE-model-prototype.patch \
        "
S = "${WORKDIR}/git"

COMPATIBLE_HOST_mipsarchn32 = "null"
COMPATIBLE_HOST_mipsarchn64 = "null"

do_install_append() {
    # Prevent QA warnings about installed ${localstatedir}/run
    if [ -d ${D}${localstatedir}/run ]; then rmdir ${D}${localstatedir}/run; fi
}
