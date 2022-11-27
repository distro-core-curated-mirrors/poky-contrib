SUMMARY = "initramfs-framework module for bmap-tools installation option"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"
RDEPENDS_${PN} = "\
    initramfs-framework-base \
    \
    bmap-tools \
    e2fsprogs-mke2fs \
    e2fsprogs-resize2fs \
    dosfstools \
    gptfdisk \
    util-linux-blkid \
    util-linux-partx \
    \
    ${VIRTUAL-RUNTIME_base-utils}"
RRECOMMENDS_${PN} = "${VIRTUAL-RUNTIME_base-utils-syslog}"

PR = "r1"

SRC_URI = "file://init-install-bmap.sh"

S = "${WORKDIR}"

# This is kind of a hack to avoid adding a new wic plugin and patching grub-efi-cfg.bbclass
do_install() {
    install -d ${D}/init.d
    install -m 0755 ${WORKDIR}/init-install-bmap.sh ${D}/init.d/install-efi.sh
}

FILES:${PN} = "/init.d/install-efi.sh"
