SUMMARY = "Matchbox Weston Desktop Plugin"
HOMEPAGE = "https://github.com/JPEWdev/weston-desktop-matchbox"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=3a4f0ddc5da2c09ab3a32fc67a1bcd1f"

DEPENDS = "\
    cairo \
    glib-2.0 \
    wayland \
    wayland-native \
    wayland-protocols \
    "

SRC_URI = "git://github.com/JPEWdev/weston-desktop-matchbox.git;protocol=http;branch=${BRANCH}"
BRANCH = "main"
SRCREV = "d8c73624254a3ac14b44b8a74bb32bbfe098dd40"

inherit pkgconfig meson

RDEPENDS:${PN} += "weston"
