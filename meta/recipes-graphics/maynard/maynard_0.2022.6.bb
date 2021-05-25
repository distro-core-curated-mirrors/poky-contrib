SUMMARY = "Maynard Wayland compositor"
LICENSE = "MIT & GPLv2+"
LIC_FILES_CHKSUM = "file://LICENSE;md5=5b570a7f9c95c7fda0f28705df2c964f"

DEPENDS = "alsa-lib weston gnome-desktop3 gtk+3 pixman wayland wayland-native glib-2.0-native"

SRC_URI = "git://gitlab.apertis.org/pkg/maynard.git;protocol=https;nobranch=1"
SRCREV = "06748347b524f429ae51389eb391b4a382fa71b9"

inherit meson pkgconfig gsettings

S = "${WORKDIR}/git"

PACKAGECONFIG ??= "gnomemenu"
PACKAGECONFIG[gnomemenu] = "-Denable-gnome-menu=enabled,-Denable-gnome-menu=disabled,gnome-menus3"
