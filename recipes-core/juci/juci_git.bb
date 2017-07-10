# Copyright (C) 2016 Khem Raj <raj.khem@gmail.com>
# Released under the MIT license (see COPYING.MIT for the terms)

DESCRIPTION = "JUCI JavaScript Webgui for embedded devices running OpenWRT"
HOMEPAGE = "https://github.com/mkschreder/juci"
LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://COPYING;md5=87212b5f1ae096371049a12f80034f32"
SECTION = "apps"

SRCREV = "${AUTOREV}"
SRC_URI = "git://github.com/mkschreder/juci"
SRC_URI += "file://0002-fix-bootstrap.patch"
SRC_URI += "file://0003-fix-juci-compile.patch"
SRC_URI += "file://0005-makefile-local.patch"

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

# PARALLEL_MAKE is required because the Makefile from Juci seems to be broken as "make -j8" would cause it to fail. Hence, forcing it to only build with -j1
PARALLEL_MAKE = "-j1"

do_install_append() {
	oe_runmake
	oe_runmake DESTDIR='${D}' install
}

FILES_${PN} += "/www ${datadir}/lua"
FILES_${PN} += "${libdir}/*"
FILES_${PN} += "${datadir}/*"
