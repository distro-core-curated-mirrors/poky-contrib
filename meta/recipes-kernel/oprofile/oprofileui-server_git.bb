require oprofileui.inc

<<<<<<< HEAD
SRCREV = "f168b8bfdc63660033de1739c6ddad1abd97c379"
PV = "0.0+git${SRCPV}"

S = "${WORKDIR}/git"

SRC_URI = "git://git.yoctoproject.org/oprofileui \
           file://init \
           file://oprofileui-server.service "
=======
SRCREV = "82ecf8c6b53b84f80682a8312f9defa83a95f2a3"
PV = "0.0+git${SRCPV}"
PR = "r0"

S = "${WORKDIR}/git"

SRC_URI = "git://git.yoctoproject.org/oprofileui;protocol=git \
           file://init"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

EXTRA_OECONF += "--disable-client --enable-server"

RDEPENDS_${PN} = "oprofile"

do_install_append() {
	install -d ${D}${sysconfdir}/init.d
	install -m 0755 ${WORKDIR}/init ${D}${sysconfdir}/init.d/oprofileui-server
<<<<<<< HEAD

	install -d ${D}${systemd_unitdir}/system
	install -m 0644 ${WORKDIR}/oprofileui-server.service ${D}${systemd_unitdir}/system/
	sed -i -e 's,@SYSCONFDIR@,${sysconfdir},g' \
		-e 's,@BINDIR@,${bindir},g' ${D}${systemd_unitdir}/system/oprofileui-server.service
}

inherit update-rc.d systemd

INITSCRIPT_NAME = "oprofileui-server"
INITSCRIPT_PARAMS = "start 99 5 2 . stop 20 0 1 6 ."

SYSTEMD_SERVICE_${PN} = "oprofileui-server.service"
SYSTEMD_AUTO_ENABLE = "disable"
=======
}

INITSCRIPT_NAME = "oprofileui-server"
INITSCRIPT_PARAMS = "start 999 5 2 . stop 20 0 1 6 ."

inherit update-rc.d
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
