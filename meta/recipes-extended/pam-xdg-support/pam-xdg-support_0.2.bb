SUMMARY = "PAM hook to create XDG_RUNTIME_DIR on login"
HOMEPAGE = "https://launchpad.net/pam-xdg-support"
LICENSE = "LGPLv3"
LIC_FILES_CHKSUM = "file://COPYING;md5=e6a600fd5e1d9cbde2d983680233ad02 \
                    file://pam_xdg_support.c;beginline=1;endline=21;md5=5c28ea20c0fa549a9b3c48e1d147546f"

SRC_URI = "http://archive.ubuntu.com/ubuntu/pool/main/p/${BPN}/${BPN}_${PV}.orig.tar.bz2 \
           file://remove-dbus.patch;pnum=0 \
           file://add-ar.patch;pnum=0 \
           file://CVE-2013-1052.patch \
           file://volatiles"

SRC_URI[md5sum] = "1311fdb880ed61301fb559e822ef0793"
SRC_URI[sha256sum] = "cb240bcc80f7f6fed326b3f392b7a491992c12c247ad926ba0f8b63ee64da8f2"

DEPENDS = "libpam"

inherit autotools

do_install_append () {
	install -d ${D}${sysconfdir}/default/volatiles
	install -m 0644 ${WORKDIR}/volatiles ${D}${sysconfdir}/default/volatiles/99_pam_xdg_support
}

FILES_${PN} += "${base_libdir}/security/*.so"
FILES_${PN}-dbg += "${base_libdir}/security/.debug"

RDEPENDS_${PN} += "libpam-runtime"

pkg_postinst_${PN} () {
	set -e
	add_xdg_module () {
		grep -q pam_xdg_support "$1" || echo "session optional pam_xdg_support.so" >> "$1"
	}
	add_xdg_module $D${sysconfdir}/pam.d/common-session
	add_xdg_module $D${sysconfdir}/pam.d/common-session-noninteractive
}

pkg_prerm_${PN} () {
	set -e
	remove_xdg_module () {
		sed -i "/pam_xdg_support\.so/d" "$1"
	}
	remove_xdg_module $D${sysconfdir}/pam.d/common-session
	remove_xdg_module $D${sysconfdir}/pam.d/common-session-noninteractive
}
