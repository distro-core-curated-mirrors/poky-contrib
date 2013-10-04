require pseudo.inc

<<<<<<< HEAD
SRCREV = "b9eb2b5633b5a23efe72c950494728d93c2b5823"
PV = "1.5.1+git${SRCPV}"
PR = "r0"

DEFAULT_PREFERENCE = "-1"

SRC_URI = "git://git.yoctoproject.org/pseudo"
=======
SRCREV = "398a264490713c912b4ce465251a8a82a7905f45"
PV = "1.4.1+git${SRCPV}"
PR = "r28"

DEFAULT_PREFERENCE = "-1"

SRC_URI = "git://git.yoctoproject.org/pseudo;protocol=git"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

S = "${WORKDIR}/git"

