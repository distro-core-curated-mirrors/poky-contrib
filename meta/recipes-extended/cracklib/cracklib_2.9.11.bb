SUMMARY = "Password strength checker library"
HOMEPAGE = "https://github.com/cracklib/cracklib"
DESCRIPTION = "${SUMMARY}"

LICENSE = "LGPL-2.1-or-later"
LIC_FILES_CHKSUM = "file://COPYING.LIB;md5=e3eda01d9815f8d24aae2dbd89b68b06"

DEPENDS = "cracklib-native zlib"

EXTRA_OECONF = "--without-python --libdir=${base_libdir}"

SRC_URI = "git://github.com/cracklib/cracklib;protocol=https;branch=main \
           file://0001-packlib.c-support-dictionary-byte-order-dependent.patch \
           "

SRCREV = "4cf5125250c6325ef0a2dc085eabff875227edc3"
S = "${WORKDIR}/git/src"

inherit autotools gettext

# This file needs to exist but isn't part of the git repo (https://github.com/cracklib/cracklib/issues/76)
do_configure:prepend() {
    mkdir -p ${S}/m4
    touch ${S}/m4/Makefile.am
}

do_install:append:class-target() {
	create-cracklib-dict -o ${D}${datadir}/cracklib/pw_dict ${D}${datadir}/cracklib/cracklib-small
}

BBCLASSEXTEND = "native nativesdk"

# TODO
# - remove libdir
# - add python support
