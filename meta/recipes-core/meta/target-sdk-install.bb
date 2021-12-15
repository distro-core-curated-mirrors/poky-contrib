SUMMARY = "Repacks a SDK shell archive into a target package"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file:///home/alex/development/poky/build-gcc-cross/tmp/deploy/sdk/poky-glibc-aarch64-core-image-minimal-core2-64-qemux86-64-toolchain-3.4+snapshot.sh"

do_install() {
    ${WORKDIR}/home/alex/development/poky/build-gcc-cross/tmp/deploy/sdk/poky-glibc-aarch64-core-image-minimal-core2-64-qemux86-64-toolchain-3.4+snapshot.sh -y -d ${D}/sdk/ -f
}

INSANE_SKIP:${PN} = "already-stripped arch ldflags staticdev dev-so"
INHIBIT_SYSROOT_STRIP = "1"
INHIBIT_PACKAGE_STRIP = "1"
INHIBIT_PACKAGE_DEBUG_SPLIT = "1"

FILES:${PN} = "/sdk"
RDEPENDS:${PN} += "bash python3-core"

EXCLUDE_PACKAGES_FROM_SHLIBS = "${PN}"
