SUMMARY = "Yocto Project documentation"
LICENSE = "CC-BY-SA-2.0"

LIC_FILES_CHKSUM = "file://documentation/index.rst;md5=55403fc485b6133f28bb4efc503ee565"

SRC_URI = "git://git.yoctoproject.org/yocto-docs"
SRCREV =  "${AUTOREV}"

DEPENDS = "make-native python3-sphinx-native python3-sphinx-rtd-theme-native python3-pyyaml-native"

PV = "3.2-git${SRCPV}"

S = "${WORKDIR}/git"
B = "${WORKDIR}/build"

inherit python3native

do_configure[noexec] = "1"

do_compile () {
    cd ${S}/documentation
    make BUILDDIR=${B} html
}

do_install () {
    install -d ${D}${docdir}/yoctoproject

    cd ${S}/documentation

    # Setting DESTDIR seems not to work as expected.
    make BUILDDIR=${B}  publish
    cp -a ${B}/final/* ${D}/${docdir}/yoctoproject
}

PACKAGES = "${PN}"
FILES_${PN} += "${docdir}/yoctoproject"

BBCLASSEXTEND = "native nativesdk"
