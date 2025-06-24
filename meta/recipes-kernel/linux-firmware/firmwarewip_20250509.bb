# if we can generate all information this isn't needed!
LICENSE = "WHENCE"
NO_GENERIC_LICENSE[WHENCE] = "WHENCE"
LIC_FILES_CHKSUM = "file://WHENCE;md5=e9abc9642f216376bb4b9080c6a3590b"

SRC_URI = "git://gitlab.com/kernel-firmware/linux-firmware.git;protocol=https;branch=main"
SRCREV = "49c833a10ad96a61a218d28028aed20aeeac124c"

S = "${UNPACKDIR}/firmwarewip-${PV}"

inherit allarch

CLEANBROKEN = "1"

PACKAGECONFIG ??= "deduplicate"
PACKAGECONFIG[deduplicate] = ",,rdfind-native"

do_compile() {
	:
}

do_install() {
        sed -i 's:^./check_whence.py:#./check_whence.py:' ${S}/copy-firmware.sh

        oe_runmake 'DESTDIR=${D}' 'FIRMWAREDIR=${nonarch_base_libdir}/firmware' install -j1

        if [ "${@bb.utils.contains('PACKAGECONFIG', 'deduplicate', '1', '0', d)}" = "1" ]; then
                oe_runmake 'DESTDIR=${D}' 'FIRMWAREDIR=${nonarch_base_libdir}/firmware' dedup
        fi
}

# Firmware files are generally not ran on the CPU, so they can be
# allarch despite being architecture specific
INSANE_SKIP = "arch"

# Don't warn about already stripped files
INSANE_SKIP:${PN} = "already-stripped"

# No need to put firmware into the sysroot
SYSROOT_DIRS_IGNORE += "${nonarch_base_libdir}/firmware"

FILES:${PN} = "${nonarch_base_libdir}/firmware/WHENCE"

require packaging.inc
