SUMMARY = "Library for rendering SVG files"
DESCRIPTION = "A small library to render Scalable Vector Graphics (SVG), \
associated with the GNOME Project. It renders SVG files to Cairo surfaces. \
Cairo is the 2D, antialiased drawing library that GNOME uses to draw things to \
the screen or to generate output for printing."
HOMEPAGE = "https://gitlab.gnome.org/GNOME/librsvg"
BUGTRACKER = "https://gitlab.gnome.org/GNOME/librsvg/issues"

LICENSE = "LGPLv2+"
LIC_FILES_CHKSUM = "file://COPYING.LIB;md5=4fbd65380cdd255951079008b364516c"

SECTION = "x11/utils"
DEPENDS = "cairo gdk-pixbuf glib-2.0 libcroco libxml2 pango"
BBCLASSEXTEND = "native nativesdk"

inherit autotools gettext gnomebase gobject-introspection gtk-doc pixbufcache upstream-version-is-even cargo
CARGO_DISABLE_BITBAKE_VENDORING = "1"

SRC_URI[archive.sha256sum] = "9bd9799322e06cf5db19b9f7afb728edac6efcf0110baafc44f0f96f45df9a09"

CACHED_CONFIGUREVARS = "ac_cv_path_GDK_PIXBUF_QUERYLOADERS=${STAGING_LIBDIR_NATIVE}/gdk-pixbuf-2.0/gdk-pixbuf-query-loaders"

PACKAGECONFIG ??= ""
# PACKAGECONFIG ??= "gdkpixbuf"
# The gdk-pixbuf loader
PACKAGECONFIG[gdkpixbuf] = "--enable-pixbuf-loader,--disable-pixbuf-loader,gdk-pixbuf-native"
# GTK+ test application (rsvg-view)

do_install_append() {
	# Loadable modules don't need .a or .la on Linux
	rm -f ${D}${libdir}/gdk-pixbuf-2.0/*/loaders/*.a ${D}${libdir}/gdk-pixbuf-2.0/*/loaders/*.la
}

PACKAGES =+ "librsvg-gtk rsvg"
FILES_rsvg = "${bindir}/rsvg* \
	      ${datadir}/pixmaps/svg-viewer.svg \
	      ${datadir}/themes"
FILES_librsvg-gtk = "${libdir}/gdk-pixbuf-2.0/*/*/*.so \
                     ${datadir}/thumbnailers/librsvg.thumbnailer"
RRECOMMENDS_librsvg-gtk = "gdk-pixbuf-bin"

PIXBUF_PACKAGES = "librsvg-gtk"
