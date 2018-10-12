SUMMARY = "C Library for manipulating module metadata files"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://COPYING;md5=25a3927bff3ee4f5b21bcb0ed3fcd6bb"

SRC_URI = "https://github.com/fedora-modularity/libmodulemd/releases/download/libmodulemd-${PV}/modulemd-${PV}.tar.xz \
           file://0001-modulemd-disable-clang-format-and-missing-dependenci.patch \
           file://0002-modulemd-v1-meson.build-disable-valgrind-dependency.patch \
           "
SRC_URI[md5sum] = "2df1ca0493223609f30de549a239f3c5"
SRC_URI[sha256sum] = "c1461c8a591c8a0111adc242bbb2b8cf01e43185fb5d2273238680ddb92a18f0"

S = "${WORKDIR}/modulemd-${PV}"

DEPENDS = "gtk-doc libyaml"

inherit gobject-introspection meson pkgconfig

BBCLASSEXTEND = "native nativesdk"
