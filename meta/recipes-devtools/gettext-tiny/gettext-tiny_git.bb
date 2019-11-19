SUMMARY = "gettext-tiny"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=ca854cb9bfecb1a90c83e477f9140eb3"

SRC_URI = "git://github.com/sabotage-linux/gettext-tiny;protocol=https"

PV = "0.3.1+git${SRCPV}"
SRCREV = "a76f8ad7b1b65cbaeb88120bb15bb5d59e1db07b"

S = "${WORKDIR}/git"

# TODO libintl should be an option.
# libintl=musl: tools and musl-stubs
#        =none: just tools
EXTRA_OEMAKE = "prefix=${prefix} \
                bindir=${bindir} \
                includedir=${includedir} \
                libdir=${libdir} \
                sysconfdir=${sysconfdir} \
                datarootdir=${datadir} \
                LIBINTL=NONE"

do_compile() {
	oe_runmake 
}

do_install() {
	oe_runmake DESTDIR="${D}" install
}

BBCLASSEXTEND = "native nativesdk"

# YUCK.  should have a way to use proper gettext if required.
PROVIDES = "gettext"
