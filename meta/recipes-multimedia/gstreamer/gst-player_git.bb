SUMMARY = "GStreamer playback helper library and examples"
LICENSE = "LGPL-2.0+"
LIC_FILES_CHKSUM = "file://gst-play/gst-play.c;beginline=1;endline=21;md5=b351a1e515a183a83d405468afca9178"

DEPENDS = "glib-2.0 gstreamer1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-bad gtk+3"

SRC_URI = "git://github.com/sdroege/gst-player.git \
           file://gst-player.desktop"

SRCREV = "ea90e63c1064503f9ba5d59aa4ca604f13ca5def"

S = "${WORKDIR}/git"

inherit autotools pkgconfig distro_features_check gobject-introspection

ANY_OF_DISTRO_FEATURES = "${GTK3DISTROFEATURES}"

do_configure_prepend() {
	touch ${S}/ChangeLog
}

EXTRA_OECONF += "ac_cv_path_VALGRIND=no ac_cv_path_GDB=no"

do_install_append() {
	install -m 0644 -D ${WORKDIR}/gst-player.desktop ${D}${datadir}/applications/gst-player.desktop
}

FILES_${PN} += "${datadir}/applications/*.desktop"

RDEPENDS_${PN} = "gstreamer1.0-plugins-base-playback"
RRECOMMENDS_${PN} = "gstreamer1.0-plugins-base-meta \
                     gstreamer1.0-plugins-good-meta \
                     gstreamer1.0-plugins-bad-meta \
                     ${@bb.utils.contains("LICENSE_FLAGS_WHITELIST", "commercial", "gstreamer1.0-libav", "", d)} \
                     ${@bb.utils.contains("LICENSE_FLAGS_WHITELIST", "commercial", "gstreamer1.0-plugins-ugly-meta", "", d)}"

RPROVIDES_${PN} = "gst-player-bin"
RREPLACES_${PN} = "gst-player-bin"
RCONFLICTS_${PN} = "gst-player-bin"
