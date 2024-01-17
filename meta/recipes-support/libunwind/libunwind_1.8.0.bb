SUMMARY = "Library for obtaining the call-chain of a program"
DESCRIPTION = "a portable and efficient C programming interface (API) to determine the call-chain of a program"
HOMEPAGE = "http://www.nongnu.org/libunwind"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://COPYING;md5=2d80c8ed4062b8339b715f90fa68cc9f"
DEPENDS:append:libc-musl = " libucontext"

SRC_URI = "https://github.com/libunwind/libunwind/releases/download/v${PV}/libunwind-${PV}.tar.gz \
           file://mips-byte-order.patch \
           file://mips-coredump-register.patch \
           file://0001-Handle-musl-on-PPC32.patch \
           file://linux-musl.patch \
           file://force-enable-man.patch \
           "

SRC_URI[sha256sum] = "b6b3df40a0970c8f2865fb39aa2af7b5d6f12ad6c5774e266ccca4d6b8b72268"

inherit autotools multilib_header

COMPATIBLE_HOST:riscv32 = "null"

PACKAGECONFIG ??= ""
PACKAGECONFIG[lzma] = "--enable-minidebuginfo,--disable-minidebuginfo,xz"
PACKAGECONFIG[zlib] = "--enable-zlibdebuginfo,--disable-zlibdebuginfo,zlib"

EXTRA_OECONF = "--enable-static"

# http://errors.yoctoproject.org/Errors/Details/20487/
ARM_INSTRUCTION_SET:armv4 = "arm"
ARM_INSTRUCTION_SET:armv5 = "arm"

LDFLAGS += "-Wl,-z,relro,-z,now ${@bb.utils.contains('DISTRO_FEATURES', 'ld-is-gold', ' -fuse-ld=bfd ', '', d)}"

DEPENDS:append:libc-musl:powerpc = " libatomic-ops"
LDFLAGS:append:libc-musl:powerpc = " -latomic"

SECURITY_LDFLAGS:append:libc-musl = " -lssp_nonshared"

do_install:append () {
	oe_multilib_header libunwind.h
}

BBCLASSEXTEND = "native"

# http://errors.yoctoproject.org/Errors/Build/183144/
# libunwind-1.6.2/include/tdep-aarch64/libunwind_i.h:123:47: error: passing argument 1 of '_ULaarch64_uc_addr' from incompatible pointer type [-Wincompatible-pointer-types]
# libunwind-1.6.2/src/aarch64/Ginit.c:348:28: error: initialization of 'unw_tdep_context_t *' from incompatible pointer type 'ucontext_t *' [-Wincompatible-pointer-types]
# libunwind-1.6.2/src/aarch64/Ginit.c:377:28: error: initialization of 'unw_tdep_context_t *' from incompatible pointer type 'ucontext_t *' [-Wincompatible-pointer-types]
# libunwind-1.6.2/src/aarch64/Ginit_local.c:51:9: error: assignment to 'ucontext_t *' from incompatible pointer type 'unw_context_t *' {aka 'unw_tdep_context_t *'} [-Wincompatible-pointer-types]
# libunwind-1.6.2/src/aarch64/Gresume.c:37:28: error: initialization of 'unw_tdep_context_t *' from incompatible pointer type 'ucontext_t *' [-Wincompatible-pointer-types]
CFLAGS += "-Wno-error=incompatible-pointer-types"
