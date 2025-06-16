LICENSE = "WHENCE"

LIC_FILES_CHKSUM = "file://WHENCE;md5=${WHENCE_CHKSUM}"
# WHENCE checksum is defined separately to ease overriding it if
# class-devupstream is selected.
WHENCE_CHKSUM  = "d85e2f182f489a235400712cbfdb017a"
NO_GENERIC_LICENSE[WHENCE] = "WHENCE"

SRC_URI = "\
  ${KERNELORG_MIRROR}/linux/kernel/firmware/linux-firmware-${PV}.tar.xz \
"

SRC_URI[sha256sum] = "f2c60d66f226a28130cb5643e6e544d3229673460e127c91ba03f1080cbd703e"

S = "${WORKDIR}/linux-firmware-${PV}"

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

        #cp LICEN[CS]E.* WHENCE ${D}${nonarch_base_libdir}/firmware/
        #cp wfx/LICEN[CS]E.* ${D}${nonarch_base_libdir}/firmware/wfx/
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
