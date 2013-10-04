DESCRIPTION = "Mobile Broadband Service Provider Database"
SECTION = "network"
LICENSE = "PD"
LIC_FILES_CHKSUM = "file://COPYING;md5=87964579b2a8ece4bc6744d2dc9a8b04"
<<<<<<< HEAD
SRCREV = "4ed19e11c2975105b71b956440acdb25d46a347d"
PV = "20120614+gitr${SRCPV}"
PE = "1"
PR = "r0"

SRC_URI = "git://git.gnome.org/mobile-broadband-provider-info"
=======
SRCREV = "d9995ef693cb1ea7237f928df18e03cccba96f16"
PV = "1.0.0+gitr${SRCPV}"
PE = "1"
PR = "r0"

SRC_URI = "git://git.gnome.org/mobile-broadband-provider-info;protocol=git"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
S = "${WORKDIR}/git"

inherit autotools
