SUMMARY = "gettext-tiny"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=ca854cb9bfecb1a90c83e477f9140eb3"

SRC_URI = "git://github.com/sabotage-linux/gettext-tiny;protocol=https"

PV = "0.3.1+git${SRCPV}"
SRCREV = "a76f8ad7b1b65cbaeb88120bb15bb5d59e1db07b"

S = "${WORKDIR}/git"

do_compile() {
	oe_runmake
}

do_install() {
	oe_runmake DESTDIR="${D}" prefix="${prefix}" libdir="${libdir}" install
}

BBCLASSEXTEND = "native nativesdk"
