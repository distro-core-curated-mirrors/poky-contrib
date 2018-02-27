require systemd.inc
FILESEXTRAPATHS =. "${FILE_DIRNAME}/systemd:"

DEPENDS = "intltool-native libcap util-linux gnu-efi gperf-native"

SRC_URI += "file://0003-use-lnr-wrapper-instead-of-looking-for-relative-opti.patch \
            file://0027-remove-nobody-user-group-checking.patch \
            file://0001-Also-check-i586-for-ia32.patch \
            file://0001-Fix-to-run-efi_cc-and-efi_ld-correctly-when-cross-co.patch \
            "

inherit meson pkgconfig gettext
inherit deploy

EFI_CC ?= "${CC}"

EXTRA_OEMESON += "-Defi=true \
                  -Dgnu-efi=true \
                  -Defi-includedir=${STAGING_INCDIR}/efi \
                  -Defi-ldsdir=${STAGING_LIBDIR} \
                  -Defi-libdir=${STAGING_LIBDIR} \
                  -Dman=false \
                  -Defi-cc='${EFI_CC}' \
                  -Defi-ld='${LD}' \
                  "


# Imported from the old gummiboot recipe
TUNE_CCARGS_remove = "-mfpmath=sse"
COMPATIBLE_HOST = "(x86_64.*|i.86.*)-linux"
COMPATIBLE_HOST_x86-x32 = "null"

do_compile() {
	SYSTEMD_BOOT_EFI_ARCH="ia32"
	if [ "${TARGET_ARCH}" == "x86_64" ]; then
		SYSTEMD_BOOT_EFI_ARCH="x64"
	fi
	ninja src/boot/efi/systemd-boot${SYSTEMD_BOOT_EFI_ARCH}.efi
}

do_install() {
	# Bypass systemd installation with a NOP
	:
}

do_deploy () {
	install ${B}/src/boot/efi/systemd-boot*.efi ${DEPLOYDIR}
}
addtask deploy before do_build after do_compile
