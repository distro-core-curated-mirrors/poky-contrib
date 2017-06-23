# Copyright (C) 2016 Khem Raj <raj.khem@gmail.com>
# Released under the MIT license (see COPYING.MIT for the terms)

DESCRIPTION = "JUCI JavaScript Webgui for embedded devices running OpenWRT"
HOMEPAGE = "https://github.com/mkschreder/juci"
LICENSE = "GPL-3.0"
LIC_FILES_CHKSUM = "file://COPYING;md5=87212b5f1ae096371049a12f80034f32"
SECTION = "apps"

SRCREV = "${AUTOREV}"
#SRCREV = "b4d8961595594e0754d399bb89588622813e49f1"
#SRC_URI = "git://github.com/mkschreder/juci"
SRC_URI = "git://github.com/leopck/juci.git"
#SRC_URI += "file://0001-juci-pin-grunt-to-0.4.1-for-grunt-angular-gettext.patch"
#SRC_URI += "file://0001-package-4.patch"
SRC_URI += "file://0001-package-v5.patch"
SRC_URI += "file://0002-makefile-v2.patch"
S = "${WORKDIR}/git"

inherit npm-install

#NPM_INSTALL_append = " uglify-js grunt-cli espree karma"
DEPENDS += "jucid lua5.1 grunt-cli-native gettext-native"

do_compile() {
	oe_runmake node_modules

	## Just simply workaround to create softlinks for the local node_modules to be added to the global path
	#cp -R ${WORKDIR}/git/node_modules/.bin ${WORKDIR}/git/node_modules/bakbin
	#ln -sf ${WORKDIR}/git/node_modules/ ${WORKDIR}/recipe-sysroot-native/usr/lib/node_modules
	ln -sf ${WORKDIR}/git/node_modules/grunt-cli/bin/grunt ${WORKDIR}/recipe-sysroot-native/usr/bin/grunt
	#ln -sf ${WORKDIR}/git/node_modules/mocha/bin/mocha ${WORKDIR}/recipe-sysroot-native/usr/bin/mocha
	#ln -sf ${WORKDIR}/git/node_modules/mocha/bin/_mocha ${WORKDIR}/recipe-sysroot-native/usr/bin/_mocha
	#ln -sf ${WORKDIR}/git/node_modules/bower/bin/bower ${WORKDIR}/recipe-sysroot-native/usr/bin/bower
	ln -sf ${WORKDIR}/git/node_modules/uglify-js/bin/uglifyjs ${WORKDIR}/recipe-sysroot-native/usr/bin/uglifyjs
	ln -sf ${WORKDIR}/git/node_modules/less/bin/lessc ${WORKDIR}/recipe-sysroot-native/usr/bin/lessc

## Workaround for the issue that this is a local node_modules and .bin directory cannot be used due to the fact that .bin is created by another user so no permission to access

	ln -sf ${WORKDIR}/git/node_modules/minify/bin/minify.js ${WORKDIR}/recipe-sysroot-native/usr/bin/minify

## Workaround for the double node_modules issue, this will cause the npm shrinkwrap to flag error, it is highly believed that this issue is due to ln -sf node_modules by nodejs because it creates a softlink inside the first node_modules
	rm ${WORKDIR}/git/node_modules/node_modules
}

do_install_append() {
	oe_runmake debug DEFAULT_THEME=y
	oe_runmake DESTDIR='${D}' install
}

FILES_${PN} += "/www ${datadir}/lua /usr/lib"
