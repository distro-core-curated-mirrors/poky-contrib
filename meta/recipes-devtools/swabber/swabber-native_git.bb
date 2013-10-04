DESCRIPTION = "Swabber is a tool that can help with understanding a program's use of host files."
HOMEPAGE = "http://git.yoctoproject.org/cgit/cgit.cgi/swabber"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=393a5ca445f6965873eca0259a17f833"

<<<<<<< HEAD
SRCREV = "2d1fe36fb0a4fdaae8823a9818a6785182d75e66"
=======
SRCREV = "a0792390c5d6d5a5bade7ab155c80eef3f30fa52"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
PV = "0.0+git${SRCPV}"

S = "${WORKDIR}/git"

<<<<<<< HEAD
SRC_URI = "git://git.yoctoproject.org/swabber"
=======
SRC_URI = "git://git.yoctoproject.org/swabber;protocol=git"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

inherit native

do_configure () {
	:
}

do_install() {
  oe_runmake 'DESTDIR=${D}' install
}
