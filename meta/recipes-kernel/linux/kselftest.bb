SUMMARY = "kselftest, the kernel test suite"
SECTION = "kernel"
LICENSE = "GPL-2.0-only"

DEPENDS = "rsync-native"

inherit kernelsrc kernel-arch pkgconfig

PACKAGE_ARCH = "${MACHINE_ARCH}"

# Unconventional usage of PACKAGECONFIG to control how the tests are built.
#
# Enabled should be unused, Disabled is the list of test targets which should
# be skipped if this dependency isn't present.
PACKAGECONFIG ??= "alsa libcap libcapng netlink numa openssl popt"
PACKAGECONFIG[alsa] = ",alsa,alsa-lib"
PACKAGECONFIG[bpf] = ",bpf hid,clang-native elfutils"
PACKAGECONFIG[fuse] = ",,fuse"
PACKAGECONFIG[libcap] = ",,libcap"
PACKAGECONFIG[libcapng] = ",,libcap-ng"
PACKAGECONFIG[netlink] = ",,libmnl"
PACKAGECONFIG[numa] = ",,numactl"
PACKAGECONFIG[openssl] = ",,openssl"
PACKAGECONFIG[popt] = ",,popt"

B = "${WORKDIR}/build"

do_compile[cleandirs] = "${B}"

CC:remove:aarch64 = "-mbranch-protection=standard"
SECURITY_CFLAGS = ""

SKIP_TARGETS = "${PACKAGECONFIG_CONFARGS}"

EXTRA_OEMAKE += "\
    O=${B} \
    V=1 \
    ARCH=${ARCH} \
    CROSS_COMPILE=${TARGET_PREFIX} \
    CC="${CC} ${DEBUG_PREFIX_MAP}" \
    AR="${AR}" \
    LD="${LD}" \
    HOSTPKG_CONFIG=pkg-config-native \
    SKIP_TARGETS="${SKIP_TARGETS}" \
"

# Force all tests to build successfully. Usually we just package what
# successfully builds.
# EXTRA_OEMAKE += "FORCE_TARGETS=1"

do_compile() {
	oe_runmake -C ${S}/tools/testing/selftests
}

do_install() {
	oe_runmake -C ${S}/tools/testing/selftests install INSTALL_PATH=${D}/${libexecdir}/kselftest
	# install uses rsync -a so reset the permissions
	chown -R root:root ${D}/${libexecdir}/kselftest
}

RDEPENDS:${PN} += "bash coreutils grep iproute2 python3-core python3 perl perl-module-io-handle"

# Some binaries appear to be explicitly built without debug info, and often
# don't pass LDFLAGS. As this is a testing tool this is acceptable.
INSANE_SKIP:${PN} = "ldflags already-stripped textrel"
