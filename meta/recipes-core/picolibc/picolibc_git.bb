require picolibc.inc

INHIBIT_DEFAULT_DEPS = "1"
DEPENDS = "virtual/${TARGET_PREFIX}gcc"

PROVIDES += "virtual/libc virtual/libiconv virtual/libintl"

COMPATIBLE_HOST:libc-musl:class-target = "null"
COMPATIBLE_HOST:libc-glibc:class-target = "null"

SRC_URI:append = " file://avoid_polluting_cross_directories.patch"

# This is being added by picolibc meson files as well to avoid
# early compiler tests from failing, cant remember why I added it
# to the newlib recipe but I would assume it was for the same reason
TARGET_CC_ARCH:append = " -nostdlib"

# When using RISCV64 use medany for both C library and application recipes
TARGET_CFLAGS:append:qemuriscv64 = " -mcmodel=medany"

# Use the same method that picolibc uses to bypass early compiler tests on meson,
# otherwise meson will try to compile AND run test applications, avoids:
# ../git/meson.build:35:0: ERROR: Executables created by c compiler are not runnable...
EXEWRAPPER_EXE ?= "exe_wrapper = ['sh', '-c', 'test -z \"$PICOLIBC_TEST\" || ${WORKDIR}/meson-qemuwrapper \"$@\"', '${WORKDIR}/meson-qemuwrapper']"

inherit meson

PACKAGECONFIG ??= " specsdir"
# Install GCC specs on libdir
PACKAGECONFIG[specsdir] = "-Dspecsdir=${libdir},-Dspecsdir=none"


FILES:${PN}-dev:append = " ${libdir}/*.specs ${libdir}/*.ld"

# No rpm package is actually created but -dev depends on it, avoid dnf error
DEV_PKG_DEPENDENCY:libc-picolibc = ""
