DESCRIPTION = "Matchbox Terminal"
HOMEPAGE = "http://www.matchbox-project.org/"
BUGTRACKER = "http://bugzilla.openedhand.com/"

LICENSE = "GPLv2+"
LIC_FILES_CHKSUM = "file://COPYING;md5=94d55d512a9ba36caa9b7df079bae19f \
                    file://main.c;endline=20;md5=96e39176d9e355639a0b8b1c7a840820"

DEPENDS = "gtk+ vte"
SECTION = "x11/utils"
<<<<<<< HEAD
SRCREV = "452bca253492a97a587f440289b9ab27d217353e"
=======
SRCREV = "3fc25cb811a8ed306de897edf9b930f4402f3852"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
PV = "0.0+git${SRCPV}"

<<<<<<< HEAD
SRC_URI = "git://git.yoctoproject.org/${BPN}"
=======
SRC_URI = "git://git.yoctoproject.org/${BPN};protocol=git"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

S = "${WORKDIR}/git"

inherit autotools pkgconfig
