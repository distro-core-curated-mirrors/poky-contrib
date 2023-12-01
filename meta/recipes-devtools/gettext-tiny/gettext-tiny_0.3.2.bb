SUMMARY = "stub and/or lightweight replacements of the GNU gettext suite"
HOMEPAGE = "https://github.com/sabotage-linux/gettext-tiny"
# buildroot says gpl3 for pieces
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=391e6ec1cd689ae2fba3ced0ee78947f"

# can't use tarball as xz-native needs gettext-minimal
#SRC_URI = "http://ftp.barfooze.de/pub/sabotage/tarballs/gettext-tiny-0.3.2.tar.xz"
#SRC_URI[sha256sum] = "a9a72cfa21853f7d249592a3c6f6d36f5117028e24573d092f9184ab72bbe187"

SRC_URI = "git://github.com/sabotage-linux/gettext-tiny;protocol=https;branch=master \
           file://gnulib.patch"
SRCREV = "0e62c2588742cfffd3dc81c09ecc8488c0ce25b9"

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

INHIBIT_DEFAULT_DEPS = "1"

do_compile() {
	oe_runmake 
}

do_install() {
	oe_runmake DESTDIR="${D}" install
}

BBCLASSEXTEND = "native nativesdk"

# YUCK.  should have a way to use proper gettext if required.
#PROVIDES = "gettext"
