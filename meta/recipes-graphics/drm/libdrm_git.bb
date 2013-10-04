require libdrm.inc

SRC_URI = "git://anongit.freedesktop.org/git/mesa/drm"

S = "${WORKDIR}/git"

DEFAULT_PREFERENCE = "-1"

<<<<<<< HEAD
SRCREV = "e01d68f9f3acfc35fe164283904b5d058c2ab378"
PV = "2.4.40+git${SRCPV}"
=======
SRCREV = "14db948127e549ea9234e02d8e112de3871f8f9f"
PV = "2.4.39+git${SRCPV}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
PR = "${INC_PR}.0"

