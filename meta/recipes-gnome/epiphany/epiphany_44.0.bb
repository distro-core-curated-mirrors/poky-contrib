SUMMARY = "WebKit based web browser for GNOME"
DESCRIPTION = "Epiphany is an open source web browser for the Linux desktop environment. \
It provides a simple and easy-to-use internet browsing experience."
HOMEPAGE = "https://wiki.gnome.org/Apps/Web"
BUGTRACKER = "https://gitlab.gnome.org/GNOME/epiphany"
LICENSE = "GPL-3.0-or-later"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"

DEPENDS = " \
	coreutils-native \
	desktop-file-utils-native \
	gcr \
	glib-2.0-native \
	gsettings-desktop-schemas \
	gstreamer1.0 \
	iso-codes \
	json-glib \
	libadwaita \
	libarchive \
	libdazzle \
	libhandy \
	libportal \
	libsecret \
	libsoup \
	libxml2 \
	nettle \
	sqlite3 \
	webkitgtk \
"

GNOMEBASEBUILDCLASS = "meson"
inherit gnomebase gsettings features_check gettext mime-xdg gtk-icon-cache
REQUIRED_DISTRO_FEATURES = "x11 opengl"

SRC_URI = "${GNOME_MIRROR}/${GNOMEBN}/${@oe.utils.trim_version("${PV}", 1)}/${GNOMEBN}-${PV}.tar.${GNOME_COMPRESS_TYPE};name=archive \
           file://0002-help-meson.build-disable-the-use-of-yelp.patch \
           file://migrator.patch \
           file://distributor.patch \
           "
SRC_URI[archive.sha256sum] = "aabdc9de80c409073676e00e15ba97187715e4b84bc776fe86db86d0f8140bb1"

# Developer mode enables debugging
PACKAGECONFIG[developer-mode] = "-Ddeveloper_mode=true,-Ddeveloper_mode=false"

FILES:${PN} += "${datadir}/dbus-1 ${datadir}/gnome-shell/search-providers ${datadir}/metainfo"
RDEPENDS:${PN} = "iso-codes adwaita-icon-theme gsettings-desktop-schemas"
