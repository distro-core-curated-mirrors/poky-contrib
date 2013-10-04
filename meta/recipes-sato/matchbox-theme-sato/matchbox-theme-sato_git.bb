require matchbox-theme-sato.inc

SRCREV = "f72cf4ed7d71ad9e47b0f2d3dbc593bc2f3e76f8"
PV = "0.2+git${SRCPV}"
PR = "r0"

DEFAULT_PREFERENCE = "-1"

<<<<<<< HEAD
SRC_URI = "git://git.yoctoproject.org/matchbox-sato"
=======
SRC_URI = "git://git.yoctoproject.org/matchbox-sato;protocol=git"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

EXTRA_OECONF += "${@base_contains('MACHINE_FEATURES', 'qvga', '--with-mode=qvga', '',d)}"

S = "${WORKDIR}/git"
