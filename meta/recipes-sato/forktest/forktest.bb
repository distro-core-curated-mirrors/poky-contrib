SUMMARY = "forktest"
LICENSE = "MIT"

SRC_URI = "file://forktest.c"

DEPENDS = "glib-2.0"

inherit pkgconfig

S = "${WORKDIR}"

do_configure[noexec] = "1"

do_compile() {
             ${CC} `pkg-config --cflags --libs glib-2.0` ${CFLAGS} ${LDFLAGS} -o forktest forktest.c
}

do_install() {
             mkdir --parents ${D}${bindir}
             install forktest ${D}${bindir}
}
