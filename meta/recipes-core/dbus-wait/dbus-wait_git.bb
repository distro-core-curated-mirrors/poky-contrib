DESCRIPTION = "A simple tool to wait for a specific signal over DBus"
HOMEPAGE = "http://git.yoctoproject.org/cgit/cgit.cgi/dbus-wait"
SECTION = "base"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=b234ee4d69f5fce4486a80fdaf4a4263"

DEPENDS = "dbus"

<<<<<<< HEAD
SRCREV = "6cc6077a36fe2648a5f993fe7c16c9632f946517"
PV = "0.1+git${SRCPV}"
PR = "r2"

SRC_URI = "git://git.yoctoproject.org/${BPN}"
=======
SRCREV = "1a3e1343761b30750bed70e0fd688f6d3c7b3717"
PV = "0.1+git${SRCPV}"
PR = "r2"

SRC_URI = "git://git.yoctoproject.org/${BPN};protocol=git"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

S = "${WORKDIR}/git"

inherit autotools
