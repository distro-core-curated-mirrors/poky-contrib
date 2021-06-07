SUMMARY = "Reference Wayland compositor for AGL"
DESCRIPTION = "The AGL compositor is a reference Wayland server for Automotive \
Grade Linux, using libweston as a base to provide a graphical environment for \
the automotive environment."

HOMEPAGE = "https://gerrit.automotivelinux.org/gerrit/q/project:src%252Fagl-compositor"
SECTION = "x11"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://COPYING;md5=fac6abe0003c4d142ff8fa1f18316df0"

DEPENDS = "wayland wayland-protocols wayland-native weston \
	   ${@bb.utils.contains('AGL_FEATURES', 'waltham-remoting', 'waltham waltham-transmitter-plugin', '', d)}"

SRC_URI = "git://gerrit.automotivelinux.org/gerrit/src/agl-compositor.git;protocol=https;branch=${AGL_BRANCH}"
AGL_BRANCH = "next"
SRCREV = "930be3400d6a42e348115ed2dca1ce72865b56bb"

PV = "0.0.19+git${SRCPV}"
S = "${WORKDIR}/git"

PACKAGECONFIG ?= ""
PACKAGECONFIG[policy-rba] = "-Dpolicy-default=rba,,librba,librba rba-config"
PACKAGECONFIG[policy-deny-all] = "-Dpolicy-default=deny-all,,"

inherit meson pkgconfig python3native

FILES_${PN} = " \
               ${bindir}/agl-compositor \
               ${bindir}/agl-screenshooter \
               ${datadir}/${PN}/protocols/agl-shell.xml \
               ${datadir}/${PN}/protocols/agl-shell-desktop.xml \
              "
RDEPENDS_${PN} += " ${@bb.utils.contains('AGL_FEATURES', 'waltham-remoting', 'waltham waltham-transmitter-plugin', '', d)}"
