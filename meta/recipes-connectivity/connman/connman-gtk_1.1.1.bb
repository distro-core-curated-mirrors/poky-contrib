SUMMARY = "GTK GUI for ConnMan"
HOMEPAGE = "https://github.com/jgke/connman-gtk"
SECTION = "libs/network"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://LICENSE;md5=b234ee4d69f5fce4486a80fdaf4a4263"

DEPENDS = "gtk+3 dbus-glib intltool-native"

SRCREV = "b72c6ab3bb19c07325c8e659902b046daa23c506"
SRC_URI = "git://github.com/jgke/connman-gtk.git \
           file://0001-update-schema.patch \
          "
S = "${WORKDIR}/git"

inherit gsettings meson gtk-icon-cache pkgconfig distro_features_check
ANY_OF_DISTRO_FEATURES = "${GTK3DISTROFEATURES}"

EXTRA_OEMESON = " -Duse_status_icon=true"

FILES_${PN} += "/usr/share/glib-2.0"
RDEPENDS_${PN} = "connman"
