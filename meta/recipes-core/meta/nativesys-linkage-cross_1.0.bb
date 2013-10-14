DESCRIPTION = "Linkage/Setup for native system development machine"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/LICENSE;md5=3f40d7994397109285ec7b81fdeb3b58 \
                    file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

INHIBIT_DEFAULT_DEPS = "1"

DEPENDS += "nativesys-linkage"

PROVIDES += "\
virtual/${TARGET_PREFIX}gcc \
virtual/${TARGET_PREFIX}g++ \
virtual/${TARGET_PREFIX}gcc-initial \
virtual/${TARGET_PREFIX}gcc-intermediate \
virtual/${TARGET_PREFIX}binutils \
virtual/${TARGET_PREFIX}libc-initial \
virtual/${TARGET_PREFIX}compilerlibs \
libgcc \
"

DUMMY = "\
linux-libc-headers \
virtual/${TARGET_PREFIX}libc-for-gcc \
virtual/libc \
virtual/libintl \
virtual/libiconv \
glibc-thread-db \
eglibc \
virtual/linux-libc-headers \
"

inherit cross

do_install () {
	install -d ${D}${bindir}
	for i in ar gcc ld 
	do
		ln -s /usr/bin/$i ${D}${bindir}/${TARGET_PREFIX}$i

	done
	install -d ${D}/usr/lib/
	ln -s /usr/lib/gcc ${D}/usr/lib/gcc
}