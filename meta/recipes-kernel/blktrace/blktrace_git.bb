DESCRIPTION = "blktrace - generate traces of the I/O traffic on block devices"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=393a5ca445f6965873eca0259a17f833"

DEPENDS = "libaio"

SRCREV = "d6918c8832793b4205ed3bfede78c2f915c23385"

<<<<<<< HEAD
PR = "r6"
PV = "1.0.5+git${SRCPV}"

SRC_URI = "git://git.kernel.dk/blktrace.git \
           file://ldflags.patch"
=======
PR = "r4"
PV = "1.0.5+git${SRCPV}"

SRC_URI = "git://git.kernel.dk/blktrace.git;protocol=git \
           file://blktrace-makefile.patch"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

S = "${WORKDIR}/git"

EXTRA_OEMAKE = "\
    'CC=${CC}' \
    'CFLAGS=${CFLAGS}' \
    'LDFLAGS=${LDFLAGS}' \
"
PARALLEL_MAKE = ""

do_install() {
	oe_runmake ARCH="${ARCH}" prefix=${prefix} \
		mandir=${mandir} DESTDIR=${D} install
}

