SUMMARY = "System performance tools"
DESCRIPTION = "The sysstat utilities are a collection of performance monitoring tools for Linux."
HOMEPAGE = "http://sebastien.godard.pagesperso-orange.fr/"
LICENSE = "GPLv2+"
SECTION = "console/utils"
<<<<<<< HEAD
=======
INC_PR = "r1"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

SRC_URI = "http://pagesperso-orange.fr/sebastien.godard/sysstat-${PV}.tar.gz \
		   file://99_sysstat \
		   file://0001-Update-Makefile-to-allow-for-parallel-execution.patch "

inherit autotools gettext

<<<<<<< HEAD
EXTRA_OECONF += "--disable-sensors"
EXTRA_OEMAKE += 'LFLAGS=""'

do_configure_prepend() {
    export sa_lib_dir=${libdir}/sa
}
=======
inherit autotools gettext

EXTRA_OECONF += "--disable-sensors"
EXTRA_OEMAKE += 'LFLAGS=""'
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

do_install() {
	autotools_do_install

	# don't install /var/log/sa when populating rootfs. Do it through volatile

	rm -rf ${D}/var
	install -d ${D}/etc/default/volatiles
	install -m 0644 ${WORKDIR}/99_sysstat ${D}/etc/default/volatiles
}

pkg_postinst_${PN} () {
        if [ -n "$D" ]; then
                exit 0
        fi
        if [ -e /etc/init.d/populate-volatile.sh ]; then
                /etc/init.d/populate-volatile.sh update
        fi
}


FILES_${PN} += "${libdir}/sa"
FILES_${PN}-dbg += "${libdir}/sa/.debug/"

TARGET_CC_ARCH += "${LDFLAGS}"
LDFLAGS_append_libc-uclibc = " -lintl"
