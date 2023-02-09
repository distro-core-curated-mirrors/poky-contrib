SUMMARY = "A library providing C and Python (libcURL like) API \
           for downloading linux repository metadata and packages."
HOMEPAGE = "https://github.com/rpm-software-management/librepo"
DESCRIPTION = "${SUMMARY}"
LICENSE = "LGPL-2.1-only"
LIC_FILES_CHKSUM = "file://COPYING;md5=4fbd65380cdd255951079008b364516c"

SRC_URI = "git://github.com/rpm-software-management/librepo.git;branch=master;protocol=https \
           file://0002-Do-not-try-to-obtain-PYTHON_INSTALL_DIR-by-running-p.patch \
           file://0004-Set-gpgme-variables-with-pkg-config-not-with-cmake-m.patch \
           "

SRCREV = "7955987e33ba98dddb3fc2c63bb6dc892e3505fa"

S = "${WORKDIR}/git"

# attr  https://github.com/rpm-software-management/librepo/commit/1dff9c2c8271ba7019b9a9a4d3612b6d4ff86b2b
DEPENDS = "curl glib-2.0 openssl gpgme libxml2"

inherit cmake setuptools3-base pkgconfig

EXTRA_OECMAKE = " \
    -DPYTHON_INSTALL_DIR=${PYTHON_SITEPACKAGES_DIR} \
    -DPYTHON_DESIRED=3 \
    -DENABLE_TESTS=OFF \
    -DENABLE_DOCS=OFF \
    -DWITH_ZCHUNK=OFF \
    -DENABLE_SELINUX=OFF \
"

BBCLASSEXTEND = "native nativesdk"

# TODO packageconfig for zchunk
# TODO packageconfig for python
# TODO packageconfig for docs
