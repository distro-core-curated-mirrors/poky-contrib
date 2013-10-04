SECTION = "base"
require uclibc.inc
require uclibc-git.inc

<<<<<<< HEAD
DEPENDS = "linux-libc-headers ncurses-native virtual/${TARGET_PREFIX}gcc-initial kern-tools-native"
=======
DEPENDS = "linux-libc-headers ncurses-native virtual/${TARGET_PREFIX}gcc-initial"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
PROVIDES = "virtual/${TARGET_PREFIX}libc-initial"

PACKAGES = ""
PACKAGES_DYNAMIC = ""

STAGINGCC = "gcc-cross-initial"
<<<<<<< HEAD
STAGINGCC_class-nativesdk = "gcc-crosssdk-initial"
=======
STAGINGCC_virtclass-nativesdk = "gcc-crosssdk-initial"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

do_install() {
	# Install initial headers into the cross dir
	make PREFIX=${D} DEVEL_PREFIX=${prefix}/ RUNTIME_PREFIX=/ \
		install_headers install_startfiles

        # add links to linux-libc-headers: final uclibc build need this.
        for t in linux asm asm-generic; do
                if [ -d ${D}${includedir}/$t ]; then
                    rm -rf ${D}${includedir}/$t
                fi
                ln -sf ${STAGING_DIR_TARGET}${includedir}/$t ${D}${includedir}/
        done

}
do_compile() {
	:
}

do_siteconfig () {
        :
}

<<<<<<< HEAD
do_populate_sysroot[sstate-outputdirs] = "${STAGING_DIR_TCBOOTSTRAP}/"
=======
do_populate_sysroot[sstate-outputdirs] = "${STAGING_DIR_TCBOOTSTRAP}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
