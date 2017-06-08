SUMMARY = "Microcode Control Tool"
DESCRIPTION = "The microcode_ctl utility is a companion to the IA32 microcode driver \
  The utility has two uses: \
  a) it decodes and sends new microcode to the kernel driver to be uploaded \
     to Intel IA32 family processors. (Pentium Pro, PII, Celeron, PIII, \
     Xeon, Pentium 4 etc, x86_64) \
  b) it signals the kernel driver to release any buffers it may hold \
"
HOMEPAGE = "https://pagure.io/microcode_ctl/"
SECTION = "console/utils"

LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/GPL-2.0;md5=801f80980d171dd6425610833a22dbe6"

SRC_URI = "git://pagure.io/microcode_ctl.git;protocol=https \
           file://0001-add-support-for-other-distributions.patch \
           file://0001-fix-the-help-return-code.patch \
           file://fix-No-GNU_HASH-in-the-elf-binary.patch \
           file://microcode_ctl.service \
          "

SRCREV = "8c8ae77e661bdba298f256948867d5a619bf1588"

# DO NOT use the v2.x which is in the obsolete branch
PV = "v1.34+git${SRCREV}"

S = "${WORKDIR}/git"

inherit update-rc.d systemd

INITSCRIPT_PACKAGES = "microcode-ctl"
INITSCRIPT_NAME_microcode-ctl = "microcode_ctl"
INITSCRIPT_PARAMS_microcode-ctl = "start 80 2 3 4 5 . stop 20 0 1 6 ."

SYSTEMD_SERVICE_${PN} = "microcode_ctl.service"

COMPATIBLE_HOST = "(i.86|x86_64).*-linux"

FIRMWARE_DIR = "${nonarch_base_libdir}/firmware"

EXTRA_OEMAKE = "'CC=${CC}' \
                'CFLAGS+=-Wall -I${STAGING_KERNEL_DIR}/include' \
               "

do_install() {
    oe_runmake install DESTDIR=${D} PREFIX=${prefix}
    rm -rf ${D}${FIRMWARE_DIR}/amd-ucode

    install -d ${D}${systemd_system_unitdir}
    install -D -m 0644 ${WORKDIR}/microcode_ctl.service ${D}${systemd_system_unitdir}/microcode_ctl.service
    sed -i -e 's,@SBINDIR@,${sbindir},g' ${D}${systemd_system_unitdir}/microcode_ctl.service
}

# do_populate_sysroot is not needed for this package,
# otherwise, it will conflict with the linux-firmware,
do_populate_sysroot[noexec] = "1"

PACKAGES += "${PN}-firmware"

FILES_${PN}-firmware = "${FIRMWARE_DIR}/microcode.dat"

RDEPENDS_${PN} = "${PN}-firmware bash"
