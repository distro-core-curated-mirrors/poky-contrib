SUMMARY = "GNU cpio is a program to manage archives of files"
DESCRIPTION = "GNU cpio is a tool for creating and extracting archives, or copying files from one place to \
another. It handles a number of cpio formats as well as reading and writing tar files."
HOMEPAGE = "http://www.gnu.org/software/cpio/"
SECTION = "base"

DEPENDS = "texinfo-native"

SRC_URI = "${GNU_MIRROR}/cpio/cpio-${PV}.tar.gz \
    file://statdef.patch \
    "

inherit autotools gettext

S = "${WORKDIR}/cpio-${PV}"

EXTRA_OECONF += "DEFAULT_RMT_DIR=${base_sbindir}"

do_install () {
    autotools_do_install
    install -d ${D}${base_bindir}/
    mv "${D}${bindir}/cpio" "${D}${base_bindir}/cpio"
    rmdir ${D}${bindir}/
}

<<<<<<< HEAD
PACKAGES =+ "${PN}-rmt"

FILES_${PN}-rmt = "${base_sbindir}/rmt*"

inherit update-alternatives

ALTERNATIVE_PRIORITY = "100"

ALTERNATIVE_${PN} = "cpio"
ALTERNATIVE_${PN}-rmt = "rmt"
=======
inherit update-alternatives

ALTERNATIVE_PRIORITY = "100"

ALTERNATIVE_${PN} = "cpio rmt"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

ALTERNATIVE_LINK_NAME[cpio] = "${base_bindir}/cpio"

ALTERNATIVE_PRIORITY[rmt] = "50"
<<<<<<< HEAD
ALTERNATIVE_LINK_NAME[rmt] = "${base_sbindir}/rmt"
=======
ALTERNATIVE_LINK_NAME[rmt] = "${libexecdir}/rmt"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
