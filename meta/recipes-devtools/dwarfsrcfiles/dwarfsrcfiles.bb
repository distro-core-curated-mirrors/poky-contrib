SUMMARY = "A small utility for printing debug source file locations embedded in binaries"
DESCRIPTION = "${SUMMARY}"
LICENSE = "GPL-2.0-or-later"
LIC_FILES_CHKSUM = "file://dwarfsrcfiles.c;md5=59532371ea15aa959c87b5a426e3614c;beginline=1;endline=6"

SRC_URI = "file://dwarfsrcfiles.c"
BBCLASSEXTEND = "native"
DEPENDS = "elfutils"
DEPENDS:append:libc-musl = " argp-standalone"

S = "${WORKDIR}/sources"
UNPACKDIR = "${S}"

do_compile () {
	${CC} ${CFLAGS} ${LDFLAGS} -o dwarfsrcfiles ${S}/dwarfsrcfiles.c -lelf -ldw
}

do_compile:libc-musl () {
	${CC} ${CFLAGS} ${LDFLAGS} -o dwarfsrcfiles ${S}/dwarfsrcfiles.c -lelf -ldw -largp
}

do_install () {
	install -d ${D}${bindir}
	install -t ${D}${bindir} dwarfsrcfiles
}

