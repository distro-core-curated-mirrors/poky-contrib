SUMMARY = "GTK GUI for ConnMan"
HOMEPAGE = "https://github.com/jgke/connman-gtk"
SECTION = "libs/network"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=b234ee4d69f5fce4486a80fdaf4a4263"

DEPENDS = "gtk+3 dbus-glib intltool-native"

SRCREV = "6e997bb771f19c65670ac1099e21ee3e3497f4d8"
SRC_URI = "git://github.com/jgke/connman-gtk.git \
          "
S = "${WORKDIR}/git"

inherit autotools-brokensep gtk-icon-cache pkgconfig distro_features_check
ANY_OF_DISTRO_FEATURES = "${GTK3DISTROFEATURES}"

FILES_${PN} += "/usr/share/glib-2.0"
RDEPENDS_${PN} = "connman"
