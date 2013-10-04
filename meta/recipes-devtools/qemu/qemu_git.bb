require qemu.inc

<<<<<<< HEAD
SRCREV = "04024dea2674861fcf13582a77b58130c67fccd8"
=======
SRCREV = "6e4c0d1f03d6ab407509c32fab7cb4b8230f57ff"

LIC_FILES_CHKSUM = "file://COPYING;md5=441c28d2cf86e15a37fa47e15a72fbac \
                    file://COPYING.LIB;endline=24;md5=c04def7ae38850e7d3ef548588159913"

PV = "1.2+git"
PR = "r0"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

LIC_FILES_CHKSUM = "file://COPYING;md5=441c28d2cf86e15a37fa47e15a72fbac \
                    file://COPYING.LIB;endline=24;md5=c04def7ae38850e7d3ef548588159913"

<<<<<<< HEAD
PV = "1.3.0+git${SRCPV}"
PR = "r0"

SRC_URI_prepend = "git://git.qemu.org/qemu.git"
S = "${WORKDIR}/git"

DEFAULT_PREFERENCE = "-1"

COMPATIBLE_HOST_class-target_mips64 = "null"
=======
SRC_URI = "\
    git://git.qemu.org/qemu.git;protocol=git \
    file://powerpc_rom.bin \
    "
S = "${WORKDIR}/git"

DEFAULT_PREFERENCE = "-1"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
