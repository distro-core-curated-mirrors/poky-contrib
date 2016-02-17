SUMMARY = "Yocto Autobuilder"
DESCRIPTION = ""
HOMEPAGE = "http://www.yoctoproject.org"
BUGTRACKER = "https://bugzilla.yoctoproject.org"

SECTION = "autobuilder"

LICENSE = "GPLv2 & BSD-3-Clause & ZPL-2.1 & MIT"
LIC_FILES_CHKSUM = "file://COPYING;md5=eb723b61539feef013de476e68b5c50a \
                    file://COPYING.buildbot;md5=f1a88a7286502fa751ec5bc81daee0da \
                    file://COPYING.decorator;md5=9bb5e7e205a2a051d17add355516fcc5 \
                    file://COPYING.htpasswd;md5=73a6429faf1e8e58dacd3a750c7d63c6 \
                    file://COPYING.jinja2;md5=7baa781602629654eb2f98ebd8487d8c \
                    file://COPYING.setuptools;md5=ad5967baf477a8cdca716556a0ec6e58 \
                    file://COPYING.sqlalchemy;md5=3da9cfbcb788c80a0384361b4de20420 \
                    file://COPYING.tempita;md5=a204069a7fc773c781ba65ecba3b2d6b \
                    file://COPYING.twisted;md5=3da9cfbcb788c80a0384361b4de20420"

S = "${WORKDIR}/git"

AB_PASSWORD = "foobar"
AB_USER_PASSWORD = "foobar"

SRCREV = "060896ae4af50392f1cf0ec4f6e3300f30308c12"
SRC_URI = "git://git.yoctoproject.org/yocto-autobuilder.git;branch=release/2.0 \
	   file://yocto-autobuilder.service"

SRC_URI[md5sum] = "5bb3b0ff2674e29378c31ad3411170ad"
SRC_URI[sha256sum] = "fa4049f8aee283de62e283d427f2cfd35d6c369b40f7f45f947dbfd915699d63"

FILES_${PN} = "root/.htpasswd root/* lib/systemd/system/yocto-autobuilder.service"

do_install() {
    # We don't do a full install here. Most of this will occur during
    # yocto-autobuilder-setup first run.

    install -m 0644 ${S}/yocto-controller/buildbot.tac.example ${S}/yocto-controller/buildbot.tac
    install -m 0644 ${S}/yocto-worker/buildbot.tac.example ${S}/yocto-worker/buildbot.tac
    install -m 0644 ${S}/yocto-controller/controller.cfg.example ${S}/yocto-controller/controller.cfg
    install -m 0644 ${S}/config/autobuilder.conf.example ${S}/config/autobuilder.conf
    install -d ${S}/buildset-config.controller ${S}/buildset-config

    sed -i "s/<PASS>/${AB_PASSWORD}/g" ${S}/yocto-controller/controller.cfg
    sed -i "s/<PASS>/${AB_PASSWORD}/g" ${S}/yocto-controller/buildbot.tac
    sed -i "s/<PASS>/${AB_PASSWORD}/g" ${S}/yocto-worker/buildbot.tac
    sed -i "s/<HOST_ADDR>/${TARGETNAME}/" ${S}/bin/worker-init
    sed -i "s/<PASS>/${AB_PASSWORD}/" ${S}/bin/worker-init

    install -d ${D}/root/yocto-autobuilder
    touch ${D}/root/.htpasswd
    ${S}/bin/htpasswd -b ${D}/root/.htpasswd root ${AB_USER_PASSWORD}
    sed -i "s?<HTPASSWDPATH>?/root/yocto-autobuilder/.htpasswd?g" ${S}/yocto-controller/controller.cfg
    cp -r ${S}/* ${D}/root/yocto-autobuilder

    install -d ${D}/lib/systemd/system/
    install -m 0644 ${WORKDIR}/yocto-autobuilder.service ${D}/lib/systemd/system/
}
