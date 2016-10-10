FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

SRC_URI_append =" file://patchtest"

do_install_append () {
	install -m 0755 ${WORKDIR}/patchtest ${D}${sysconfdir}/init.d
	update-rc.d -r ${D} patchtest start 99 3 5 .
}


