SUMMARY = "Parallel, indexed xz compressor"

DEPENDS = "xz libarchive"

SRC_URI = "${SOURCEFORGE_MIRROR}/pixz/${BPN}-${PV}.tgz"
SRC_URI[md5sum] = "90034c862d7c9340b76611f3fb909855"
SRC_URI[sha256sum] = "af9dac41edd6bf57953471f7fcbd4793810003bf911593ba4c84f7cccb5f74af"

LICENSE = "BSD-2-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=5cf6d164086105f1512ccb81bfff1926"

# the makefile needs this to end in -o
LD = "${CC} ${LDFLAGS} -o"
LD_class-native = "${CC} ${LDFLAGS} -o"

# Some systems need -lm for ceil()
export THREADS = "-lpthread -lm"

do_install () {
	install -d ${D}${bindir}
	install ${S}/pixz ${D}${bindir}
}

BBCLASSEXTEND = "native"