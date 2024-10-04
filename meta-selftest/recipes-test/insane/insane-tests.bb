SUMMARY = "Test cases for the checks in insane.bbclass"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://textrel.c file://hello.c"

S = "${UNPACKDIR}"
B = "${WORKDIR}/build"

do_compile[cleandirs] = "${B}"
do_compile() {
    ${CC} ${CFLAGS} ${LDFLAGS} ${S}/hello.c -o ${B}/insane-bad-rpath -Wl,-rpath ${B}/bad-rpath
    ${CC} ${CFLAGS} ${LDFLAGS} ${S}/textrel.c -o ${B}/insane-textrel -fno-pic
}

do_install() {
    install -d ${D}${bindir}
    install ${B}/* ${D}${bindir}
}

# Expected errors:
# insane-textrel [textrel]
# insane-bad-rpath [buildpaths] [rpaths]

# TODO
# - redundant rpath
