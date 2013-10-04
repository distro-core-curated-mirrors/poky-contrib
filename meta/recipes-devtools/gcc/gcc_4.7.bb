require recipes-devtools/gcc/gcc-${PV}.inc
<<<<<<< HEAD
require gcc-target.inc
=======
require gcc-configure-target.inc
require gcc-package-target.inc

ARCH_FLAGS_FOR_TARGET += "-isystem${STAGING_INCDIR}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
