# Copyright (C) 2016 Khem Raj <raj.khem@gmail.com>
# Released under the MIT license (see COPYING.MIT for the terms)

DESCRIPTION = "JUCI JavaScript Webgui for embedded devices running OpenWRT"
HOMEPAGE = "https://github.com/mkschreder/juci"
LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://COPYING;md5=87212b5f1ae096371049a12f80034f32"
SECTION = "apps"

SRCREV = "b173dba22fbd9891bc5e3a55f8b40ba562f38e31"
SRC_URI = "git://github.com/mkschreder/juci"
SRC_URI += "file://0001-juci-pin-grunt-to-0.4.1-for-grunt-angular-gettext.patch"
SRC_URI += "file://0002-fix-bootstrap.patch"
SRC_URI += "file://0003-fix-juci-compile.patch"

S = "${WORKDIR}/git"

inherit npm-install

NPM_INSTALL_append = " --save uglify-js less minify"
DEPENDS += "jucid lua5.1 grunt-cli-native"

do_compile() {
	oe_runmake node_modules
}

do_compile_append(){
        ln -sf ${WORKDIR}/git/node_modules/uglify-js/bin/uglifyjs ${WORKDIR}/recipe-sysroot-native/usr/bin/uglifyjs
        ln -sf ${WORKDIR}/git/node_modules/less/bin/lessc ${WORKDIR}/recipe-sysroot-native/usr/bin/lessc
        ln -sf ${WORKDIR}/git/node_modules/.bin/minify ${WORKDIR}/recipe-sysroot-native/usr/bin/minify
}

do_install_append() {
	oe_runmake
	oe_runmake DESTDIR='${D}' install
}

FILES_${PN} += "/www ${datadir}/lua"
