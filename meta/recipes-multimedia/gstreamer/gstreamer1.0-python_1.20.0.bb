SUMMARY = "Python bindings for GStreamer 1.0"
DESCRIPTION = "GStreamer Python binding overrides (complementing the bindings \
provided by python-gi) "
HOMEPAGE = "http://cgit.freedesktop.org/gstreamer/gst-python/"
SECTION = "multimedia"

LICENSE = "LGPLv2.1"
LIC_FILES_CHKSUM = "file://COPYING;md5=c34deae4e395ca07e725ab0076a5f740"

require gstreamer1.0-source.inc

S = "${SRC_BASE}/subprojects/gst-python"

DEPENDS = "gstreamer1.0 gstreamer1.0-plugins-base python3-pygobject"
RDEPENDS:${PN} += "gstreamer1.0 gstreamer1.0-plugins-base python3-pygobject"

PNREAL = "gst-python"

EXTRA_OEMESON += "-Dlibpython-dir=${libdir}"

# gobject-introspection is mandatory and cannot be configured
REQUIRED_DISTRO_FEATURES = "gobject-introspection-data"
GIR_MESON_OPTION = ""

inherit meson pkgconfig setuptools3-base upstream-version-is-even gobject-introspection features_check
