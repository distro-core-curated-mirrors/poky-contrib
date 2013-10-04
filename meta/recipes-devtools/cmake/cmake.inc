# Copyright (C) 2005, Koninklijke Philips Electronics NV.  All Rights Reserved
# Released under the MIT license (see packages/COPYING)

DESCRIPTION = "A cross-platform, open-source make system"
HOMEPAGE = "http://www.cmake.org/"
BUGTRACKER = "http://public.kitware.com/Bug/my_view_page.php"
SECTION = "console/utils"
LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://Copyright.txt;md5=bb2fa3a08736b842556f6171bb9e8ae1 \
                    file://Source/cmake.h;beginline=1;endline=10;md5=341736dae83c9e344b53eeb1bc7d7bc2"

<<<<<<< HEAD
CMAKE_MAJOR_VERSION = "${@'.'.join(d.getVar('PV',1).split('.')[0:2])}"

SRC_URI = "http://www.cmake.org/files/v${CMAKE_MAJOR_VERSION}/cmake-${PV}.tar.gz \
           file://support-oe-qt4-tools-names.patch \
           file://aarch64-cmake.patch \
           file://aarch64-kwsys.patch \
           file://qt4-fail-silent.patch \
           "
=======
INC_PR = "r0"

CMAKE_MAJOR_VERSION = "${@'.'.join(d.getVar('PV',1).split('.')[0:2])}"

SRC_URI = "http://www.cmake.org/files/v${CMAKE_MAJOR_VERSION}/cmake-${PV}.tar.gz \
           file://support-oe-qt4-tools-names.patch"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

inherit autotools

do_configure () {
	./configure --prefix=${prefix}
}
