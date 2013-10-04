require x-load.inc

<<<<<<< HEAD
FILESPATH = "${FILE_DIRNAME}/x-load-git/${MACHINE}:${FILE_DIRNAME}/x-load-git/"
=======
FILESDIR = "${@os.path.dirname(d.getVar('FILE',1))}/x-load-git/${MACHINE}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

LICENSE = "GPLv2+"
LIC_FILES_CHKSUM = "file://README;beginline=1;endline=25;md5=ef08d08cb99057bbb5b9d6d0c5a4396f"

SRCREV = "9f94c6577e3a018b6b75cbe39f32bb331871f915"
PV = "1.5.0+git${SRCPV}"
PR="r0"

#SRC_URI = "git://www.sakoman.net/git/x-load-omap3.git;branch=master"
#SRC_URI = "git://gitorious.org/x-load-omap3/mainline.git;branch=master"
SRC_URI = "git://gitorious.org/x-loader/x-loader.git;branch=master"

SRC_URI_append_beagleboard = " file://name.patch "

<<<<<<< HEAD
=======
SRC_URI_append_beagleboard = " file://name.patch "

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
S = "${WORKDIR}/git"

PACKAGE_ARCH = "${MACHINE_ARCH}"

COMPATIBLE_MACHINE = "(beagleboard|omap3evm|overo)"
