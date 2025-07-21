LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://docs/license.rst;md5=ffe678546d4337b732cfd12262e6af11"

SRC_URI = "https://archive.mesa3d.org/mesa-${PV}.tar.xz \
           file://0001-meson-misdetects-64bit-atomics-on-mips-clang.patch \
           file://0001-freedreno-don-t-encode-build-path-into-binaries.patch \
           file://0001-dont-build-clover-frontend.patch \
"

SRC_URI[sha256sum] = "3c4f6b10ff6ee950d0ec6ea733cc6e6d34c569454e3d39a9b276de9115a3b363"
PV = "25.1.5"

UPSTREAM_CHECK_GITTAGREGEX = "mesa-(?P<pver>\d+(\.\d+)+)"

S = "${UNPACKDIR}/mesa-${PV}"

PROVIDES = "virtual/libgbm"

DEPENDS = "libdrm"

inherit meson pkgconfig

EXTRA_OEMESON = "\
    --auto-features=disabled \
    -Dgbm=enabled \
    -Dopengl=false -Degl=disabled -Dglx=disabled \
    -Dplatforms= -Dgallium-drivers= -Dvulkan-drivers= -Dvulkan-layers="

BBCLASSEXTEND = "native nativesdk"

# TODO GRRR
inherit python3native
DEPENDS += "python3-mako-native python3-pyyaml-native"
