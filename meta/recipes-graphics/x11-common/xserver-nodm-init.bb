SUMMARY = "Simple Xserver Init Script (no dm)"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=751419260aa954499f7abaabaa882bbe"
SECTION = "x11"
<<<<<<< HEAD
PR = "r31"

SRC_URI = "file://xserver-nodm \
           file://Xusername \
           file://gplv2-license.patch \
           file://xserver-nodm.service \
           file://xserver-nodm.conf \
"

S = "${WORKDIR}"

# Since we refer to ROOTLESS_X which is normally enabled per-machine
PACKAGE_ARCH = "${MACHINE_ARCH}"

inherit update-rc.d systemd

do_install() {
    install -d ${D}${sysconfdir}/init.d
    install xserver-nodm ${D}${sysconfdir}/init.d

    if ${@base_contains('DISTRO_FEATURES','systemd','true','false',d)}; then
        install -d ${D}${sysconfdir}/default
        install xserver-nodm.conf ${D}${sysconfdir}/default/xserver-nodm
        install -d ${D}${systemd_unitdir}/system
        install -m 0644 ${WORKDIR}/xserver-nodm.service ${D}${systemd_unitdir}/system
        if [ "${ROOTLESS_X}" = "1" ] ; then
            sed -i 's!^HOME=.*!HOME=/home/xuser!' ${D}${sysconfdir}/default/xserver-nodm
            sed -i 's!^User=.*!User=xuser!' ${D}${systemd_unitdir}/system/xserver-nodm.service
        else
            sed -i 's!^HOME=.*!HOME=${ROOT_HOME}!' ${D}${sysconfdir}/default/xserver-nodm
            sed -i '/^User=/d' ${D}${systemd_unitdir}/system/xserver-nodm.service
        fi
    fi

    if ${@base_contains('DISTRO_FEATURES','sysvinit','true','false',d)}; then
        if [ "${ROOTLESS_X}" = "1" ] ; then
            install -d ${D}${sysconfdir}/X11
            install Xusername ${D}${sysconfdir}/X11
        fi
    fi
}

RDEPENDS_${PN} = "${@base_conditional('ROOTLESS_X', '1', 'xuser-account', '', d)}"

INITSCRIPT_NAME = "xserver-nodm"
INITSCRIPT_PARAMS = "start 9 5 2 . stop 20 0 1 6 ."
SYSTEMD_SERVICE_${PN} = "xserver-nodm.service"
=======
PR = "r30"
RDEPENDS_${PN} = "sudo"

SRC_URI = "file://xserver-nodm \
           file://Xusername \
           file://gplv2-license.patch"

S = "${WORKDIR}"

PACKAGE_ARCH = "${MACHINE_ARCH}"

do_install() {
    install -d ${D}${sysconfdir}
    install -d ${D}${sysconfdir}/init.d
    install xserver-nodm ${D}${sysconfdir}/init.d
    if [ "${ROOTLESS_X}" = "1" ] ; then
        install -d ${D}${sysconfdir}/X11
        install Xusername ${D}${sysconfdir}/X11
    fi
}

inherit update-rc.d useradd

INITSCRIPT_NAME = "xserver-nodm"
INITSCRIPT_PARAMS = "start 9 5 2 . stop 20 0 1 6 ."

# Use fixed Xusername of xuser for now, this will need to be
# fixed if the Xusername changes from xuser
# IMPORTANT: because xuser is shared with connman, please make sure the
# USERADD_PARAM is in sync with the one in connman.inc
USERADD_PACKAGES = "${PN}"
USERADD_PARAM_${PN} = "--create-home \
                       --groups video,tty,audio \
                       --user-group xuser"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

