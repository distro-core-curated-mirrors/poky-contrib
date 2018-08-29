SUMMARY = "GLib networking extensions"
DESCRIPTION = "glib-networking contains the implementations of certain GLib networking features that cannot be implemented directly in GLib itself because of their dependencies."
HOMEPAGE = "http://git.gnome.org/browse/glib-networking/"
BUGTRACKER = "http://bugzilla.gnome.org"

LICENSE = "LGPL-2.1"
LIC_FILES_CHKSUM = "file://COPYING;md5=4fbd65380cdd255951079008b364516c"

SECTION = "libs"
DEPENDS = "glib-2.0 gnutls"

SRC_URI[archive.md5sum] = "456572f1e8fea32ef747541d64508a8e"
SRC_URI[archive.sha256sum] = "df47b0e0a037d2dcf6b1846cbdf68dd4b3cc055e026bb40c4a55f19f29f635c8"

PACKAGECONFIG ??= "ca-certificates"

# No explicit dependency as it works without ca-certificates installed
PACKAGECONFIG[ca-certificates] = "-Dca_certificates_path=${sysconfdir}/ssl/certs/ca-certificates.crt,"
PACKAGECONFIG[libproxy] = "-Dlibproxy_support=true,-Dlibproxy_support=false,libproxy"
PACKAGECONFIG[pkcs11] = "-Dpkcs11_support=true,-Dpkcs11_support=false,p11-kit"

EXTRA_OEMESON = "-Dgnome_proxy_support=false"

GNOMEBASEBUILDCLASS = "meson"
inherit gnomebase gettext upstream-version-is-even gio-module-cache

FILES_${PN} += "${libdir}/gio/modules/libgio*.so ${datadir}/dbus-1/services/"
FILES_${PN}-dev += "${libdir}/gio/modules/libgio*.la"
FILES_${PN}-staticdev += "${libdir}/gio/modules/libgio*.a"
