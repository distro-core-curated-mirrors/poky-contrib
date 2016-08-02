SUMMARY = "Dandified Yum"
DESCRIPTION = "Package management using RPM, libsolv and hawkey libraries. \
For metadata handling and package downloads it utilizes librepo. To process \
and effectively handle the comps data it uses libcomps."

HOMEPAGE = "http://github.com/rpm-software-management/dnf"
SECTION = "devel/python"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=b234ee4d69f5fce4486a80fdaf4a4263"

DEPENDS = "cmake python rpm gettext-native python-rpm"
SRCNAME = "dnf"

SRC_URI = "\
          git://github.com/rpm-software-management/dnf.git;branch=dnf-1.1 \
         "

SRCREV = "6f31dce3f019231edebe2ab793b52ea0ce0a4c4b"
PV = "1.1.9-1+git${SRCPV}"

S = "${WORKDIR}/git"

EXTRA_OECMAKE += " -DPYTHON_DESIRED='3' \
                   -DWITH_MAN=0 \
                 "

inherit cmake python3native

BBCLASSEXTEND = "native nativesdk"
