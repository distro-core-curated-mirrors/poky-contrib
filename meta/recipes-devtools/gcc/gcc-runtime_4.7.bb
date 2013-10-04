require recipes-devtools/gcc/gcc-${PV}.inc
<<<<<<< HEAD
require gcc-runtime.inc

=======
require gcc-configure-runtime.inc
require gcc-package-runtime.inc

ARCH_FLAGS_FOR_TARGET += "-isystem${STAGING_INCDIR}"

EXTRA_OECONF += "--disable-libunwind-exceptions"
EXTRA_OECONF_append_linuxstdbase = " --enable-clocale=gnu"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
