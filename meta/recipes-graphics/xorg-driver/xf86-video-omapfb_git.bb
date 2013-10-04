require xorg-driver-video.inc

SUMMARY = "X.Org X server -- Texas Instruments OMAP framebuffer driver"

DESCRIPTION = "omapfb driver supports the basic Texas Instruments OMAP \
framebuffer."

LICENSE = "MIT-X & GPLv2+"
LIC_FILES_CHKSUM = "file://COPYING;md5=63e2cbac53863f60e2f43343fb34367f"
DEPENDS += "virtual/libx11"

SRCREV = "28c006c94e57ea71df11ec4fff79d7ffcfc4860f"
<<<<<<< HEAD
PR = "${INC_PR}.7"
PV = "0.1.1+gitr${SRCPV}"

SRC_URI = "git://git.pingu.fi/xf86-video-omapfb;protocol=http \
  file://0001-Revert-Set-a-large-CRTC-upper-limit-to-not-prune-lar.patch \
  file://0002-Revert-Set-virtual-size-when-configuring-framebuffer.patch \
  file://0003-force-plain-mode.patch \
  file://0004-blacklist-tv-out.patch \
  file://0005-Attempt-to-fix-VRFB.patch \
  file://0006-omapfb-port-to-new-xserver-video-API.patch \
=======
PR = "${INC_PR}.6"
PV = "0.1.1+gitr${SRCPV}"

SRC_URI = "git://git.pingu.fi/xf86-video-omapfb;protocol=http \
            file://omap-revert-set-CRTC-limit.patch \
            file://omap-revert-set-virtual-size.patch \
            file://omap-force-plain-mode.patch  \
            file://omap-blacklist-tv-out.patch  \
            file://0004-Attempt-to-fix-VRFB.patch \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
"

S = "${WORKDIR}/git"

EXTRA_OECONF_armv7a = " --enable-neon "
CFLAGS += " -I${STAGING_INCDIR}/xorg "

# Use overlay 2 on omap3 to enable other apps to use overlay 1 (e.g. dmai or omapfbplay)
do_compile_prepend_armv7a () {
        sed -i -e s:fb1:fb2:g ${S}/src/omapfb-xv.c
}
