SUMMARY = "Virtual terminal emulator GTK+ widget library"
BUGTRACKER = "https://bugzilla.gnome.org/buglist.cgi?product=vte"
LICENSE = "LGPLv2.1+"
DEPENDS = "glib-2.0 gtk+3 intltool-native"

LIC_FILES_CHKSUM = "file://COPYING;md5=4fbd65380cdd255951079008b364516c"
SRC_URI[archive.md5sum] = "20916d97a5902657e54307cc2757beee"
SRC_URI[archive.sha256sum] = "712dd548339f600fd7e221d12b2670a13a4361b2cd23ba0e057e76cc19fe5d4e"

inherit gnomebase gtk-doc distro_features_check upstream-version-is-even vala gobject-introspection
ANY_OF_DISTRO_FEATURES = "${GTK3DISTROFEATURES}"

PACKAGECONFIG[gnutls] = "--with-gnutls,--without-gnutls,gnutls"

CFLAGS += "-D_GNU_SOURCE"
LDFLAGS_append = " -lssp_nonshared"

# Enable vala only if gobject-introspection is enabled
EXTRA_OECONF = "--enable-vala=auto"

PACKAGES =+ "libvte"
FILES_libvte = "${libdir}/*.so.*"
