SUMMARY = "Hello world recipe"
DESCRIPTION = "test application"
LICENSE = "CLOSED"
SRC_URI = "file://hello.c \
"
S = "${WORKDIR}"
do_compile() {
    ${CC} hello.c -o hello
}

do_install() {
    install -d ${D}/${bindir}
    install -m 0755 hello ${D}/${bindir}
}

