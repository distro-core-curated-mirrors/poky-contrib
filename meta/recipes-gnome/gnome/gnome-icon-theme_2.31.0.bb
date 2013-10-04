DESCRIPTION = "GNOME 2 default icon themes"
HOMEPAGE = "http://www.gnome.org/"
BUGTRACKER = "https://bugzilla.gnome.org/"
SECTION = "x11/gnome"

LICENSE = "LGPLv3+ | CC-BY-SA-3.0"
LIC_FILES_CHKSUM = "file://COPYING;md5=e7e289d90fc8bdceed5e3f142f98229e"

<<<<<<< HEAD
PR = "r5"
=======
SECTION = "x11/gnome"
DEPENDS = "icon-naming-utils-native glib-2.0 intltool-native"
RDEPENDS_${PN} = "hicolor-icon-theme"
RRECOMMENDS_${PN} = "librsvg-gtk"
PR = "r3"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

DEPENDS = "icon-naming-utils-native glib-2.0 intltool-native libxml-simple-perl-native"

<<<<<<< HEAD
inherit autotools perlnative gtk-icon-cache

=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
SRC_URI = "${GNOME_MIRROR}/${BPN}/2.31/${BPN}-${PV}.tar.bz2 \
           file://iconpath-option.patch"

SRC_URI[md5sum] = "8e727703343d4c18c73c79dd2009f8ed"
SRC_URI[sha256sum] = "ea7e05b77ead159379392b3b275ca0c9cbacd7d936014e447cc7c5e27a767982"

<<<<<<< HEAD
EXTRA_OECONF = "--with-iconmap=${@d.getVar('STAGING_LIBEXECDIR_NATIVE', True).replace('gnome-icon-theme', 'icon-naming-utils')}/icon-name-mapping"

FILES_${PN} += "${datadir}/*"
RRECOMMENDS_${PN} += "librsvg-gtk"
=======
EXTRA_OECONF = "--disable-hicolor-check"
EXTRA_OECONF += "--with-iconmap=${@d.getVar('STAGING_LIBEXECDIR_NATIVE', True).replace('gnome-icon-theme', 'icon-naming-utils')}/icon-name-mapping"


inherit autotools
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
