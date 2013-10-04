DESCRIPTION = "GNU Portable Threads"
HOMEPAGE = "http://www.gnu.org/software/pth/"
SECTION = "libs"
LICENSE = "GPLv2+"
LIC_FILES_CHKSUM = "file://COPYING;beginline=12;endline=15;md5=a48af114a80c222cafd37f24370a77b1"
<<<<<<< HEAD
PR = "r3"
=======
PR = "r2"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

python __anonymous () {
    import re
    uc_os = (re.match('.*uclibc*', d.getVar('TARGET_OS', True)) != None)
    if uc_os:
        raise bb.parse.SkipPackage("incompatible with uClibc")
}

SRC_URI = "${GNU_MIRROR}/pth/pth-${PV}.tar.gz \
<<<<<<< HEAD
          file://pth-add-pkgconfig-support.patch"
=======
          "
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

SRC_URI[md5sum] = "9cb4a25331a4c4db866a31cbe507c793"
SRC_URI[sha256sum] = "72353660c5a2caafd601b20e12e75d865fd88f6cf1a088b306a3963f0bc77232"

PARALLEL_MAKE=""

inherit autotools binconfig pkgconfig

do_configure() {
	( cd ${S}; gnu-configize )
	( cd ${S}; autoconf )
	oe_runconf
}
