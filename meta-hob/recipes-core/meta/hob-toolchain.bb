DESCRIPTION = "dummy toolchain"
LICENSE = "MIT"

PR = "r0"

LIC_FILES_CHKSUM = "file://${COREBASE}/LICENSE;md5=3f40d7994397109285ec7b81fdeb3b58 \
                    file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

<<<<<<< HEAD
inherit populate_sdk
=======
IMAGETEST ?= "dummy"
inherit populate_sdk imagetest-${IMAGETEST}
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
