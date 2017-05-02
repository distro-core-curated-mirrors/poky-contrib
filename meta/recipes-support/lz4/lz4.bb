SUMMARY = "Extremely Fast Compression algorithm"
DESCRIPTION = "LZ4 is a very fast lossless compression algorithm, providing compression speed at 400 MB/s per core, scalable with multi-cores CPU. It also features an extremely fast decoder, with speed in multiple GB/s per core, typically reaching RAM speed limits on multi-core systems."

LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://lib/LICENSE;md5=ebc2ea4814a64de7708f1571904b32cc"

#SRCREV = "d86dc916771c126afb797637dda9f6421c0cb998"
SRCREV = "${AUTOREV}"

#PV = "131+git${SRCPV}"
PV="git${SRCPV}"

SRC_URI = "git://github.com/Cyan4973/lz4.git;branch=master"

S = "${WORKDIR}/git"

EXTRA_OEMAKE = "PREFIX=${prefix} CC='${CC}' DESTDIR=${D} LIBDIR=${libdir} INCLUDEDIR=${includedir}"

do_install() {
	oe_runmake install
}

BBCLASSEXTEND = "native nativesdk"
