SUMMARY = "forktest"
LICENSE = "MIT"

SRC_URI = "file://forktest.c file://forktest2.c file://forklib.c file://forklib.h file://forktest3.c"

DEPENDS = "glib-2.0"

inherit pkgconfig

S = "${WORKDIR}"

do_configure[noexec] = "1"

do_compile() {
             ${CC} `pkg-config --cflags --libs glib-2.0` ${CFLAGS} ${LDFLAGS} -o forktest forktest.c
             ${CC} -lpthread -o forktest2 forktest2.c
             ${CC} -lpthread -fpic -shared -o libforklib.so forklib.c
             ${CC} -lforklib -L. -o forktest3 forktest3.c -Wl,-nostdlib
}

do_install() {
             mkdir --parents ${D}${bindir}
             install forktest ${D}${bindir}
             install forktest2 ${D}${bindir}
             install forktest3 ${D}${bindir}
             install -d ${D}${libdir}
             install libforklib.so ${D}${libdir}
}
