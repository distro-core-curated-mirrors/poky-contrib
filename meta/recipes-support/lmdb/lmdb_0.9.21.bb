SUMMARY = "Symas Lightning Memory-Mapped Database (LMDB)"
HOMEPAGE = "http://symas.com/lmdb/"
LICENSE = "OLDAP-2.8"
LIC_FILES_CHKSUM = "file://LICENSE;md5=153d07ef052c4a37a8fac23bc6031972"

SRC_URI = "git://github.com/LMDB/lmdb.git;branch=mdb.RE/0.9 \
           file://0001-Patch-the-main-Makefile.patch \
           file://lmdb.pc.in \
          "
SRCREV = "60d500206a108b2c64ca7e36b0113b2cd3711b98"
S = "${WORKDIR}/git/libraries/liblmdb"

do_compile() {
    oe_runmake "CC=${CC}"
}

do_install() {
    oe_runmake DESTDIR=${D} prefix=${prefix} libdir=${libdir} install
    chown -R root:root ${D}${bindir}
    chown -R root:root ${D}${libdir}

    # Install pkgconfig file
    # This is copied and tweaked from Fedora's spec:
    # https://src.fedoraproject.org/rpms/lmdb/blob/master/f/lmdb.spec
    # The file itself is here:
    # https://src.fedoraproject.org/rpms/lmdb/blob/master/f/lmdb.pc.in
    sed -e 's:@PREFIX@:${prefix}:g' \
    -e 's:@EXEC_PREFIX@:${exec_prefix}:g' \
    -e 's:@LIBDIR@:${libdir}:g' \
    -e 's:@INCLUDEDIR@:${includedir}:g' \
    -e 's:@PACKAGE_VERSION@:${PV}:g' \
    ${WORKDIR}/lmdb.pc.in > ${WORKDIR}/lmdb.pc

    install -Dpm 0644 -t ${D}${libdir}/pkgconfig ${WORKDIR}/lmdb.pc
}

BBCLASSEXTEND = "native"
