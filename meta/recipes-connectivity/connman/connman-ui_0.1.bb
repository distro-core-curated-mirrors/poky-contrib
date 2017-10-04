SUMMARY = "A full-featured GTK based trayicon UI for ConnMan"
HOMEPAGE = "https://github.com/tbursztyka/connman-ui"
SECTION = "libs/network"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=12f884d2ae1ff87c09e5b7ccc2c4ca7e"

DEPENDS = "gtk+3 dbus-glib intltool-native"

SRCREV = "fce0af94e121bde77c7fa2ebd6a319f0180c5516"
SRC_URI = "git://github.com/tbursztyka/connman-ui.git \
          "

S = "${WORKDIR}/git"

inherit autotools-brokensep gtk-icon-cache pkgconfig distro_features_check
ANY_OF_DISTRO_FEATURES = "${GTK3DISTROFEATURES}"

FILES_${PN} += "/usr/share/connman_ui_gtk"
RDEPENDS_${PN} = "connman"
