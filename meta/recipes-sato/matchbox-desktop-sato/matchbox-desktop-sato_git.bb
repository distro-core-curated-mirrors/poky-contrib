SUMMARY = "Matchbox desktop folders for the Sato environment"
HOMEPAGE = "http://matchbox-project.org"
BUGTRACKER = "http://bugzilla.yoctoproject.org/"

LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=59530bdf33659b29e73d4adb9f9f6552"

SECTION = "x11"
DEPENDS = ""
RCONFLICTS_${PN} = "matchbox-common"

#commit for 0.2 tag
SRCREV = "37886756886786bc65cbcbedb43c3c07b2c761e6"
PV = "0.2"

SRC_URI = "git://git.yoctoproject.org/${BPN}"
SRC_URI = "git://github.com/jku/matchbox-desktop-sato;branch=gtk3"

S = "${WORKDIR}/git"

inherit autotools pkgconfig

FILES_${PN} += "${datadir}"
