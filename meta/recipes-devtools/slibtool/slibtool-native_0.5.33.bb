LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://COPYING.SLIBTOOL;md5=1293820cb7ae16ca38db503f4b1d7693 \
                    file://COPYING.SOFORT;md5=5405af46e9363fdc2f02d40b639033a1"

SRC_URI = "git://dev.midipix.org/cross/slibtool.git;protocol=https;branch=main \
           file://soname.patch"

SRCREV = "9c5a301fe8f9f29010a625ac5e7f32d789af1a34"
PV .= "+git${SRCPV}"

inherit native

S = "${WORKDIR}/git"
B = "${WORKDIR}/build"

# TODO build/host/target, BBCLASSEXTEND

do_configure() {
	${S}/configure \
		--source-dir=${S} \
		--prefix=${prefix} \
		--libdir=${libdir} \
		--compiler="${CC}"
}

do_install () {
	oe_runmake install DESTDIR=${D}
}
