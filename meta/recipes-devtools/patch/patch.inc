SUMMARY = "Tool for applying a patch file"
DESCRIPTION = "patch takes a patch file containing a difference listing \
produced by the diff program and applies those differences to one or more \
original files, producing patched versions."
SECTION = "utils"

SRC_URI = "${GNU_MIRROR}/patch/patch-${PV}.tar.gz"
S = "${WORKDIR}/patch-${PV}"

inherit autotools update-alternatives

<<<<<<< HEAD
PACKAGECONFIG ??= ""
PACKAGECONFIG[attr] = "--enable-xattr,--disable-xattr,attr"

=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
ALTERNATIVE_${PN} = "patch"
ALTERNATIVE_PRIORITY = "100"
