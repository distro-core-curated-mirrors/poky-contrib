require recipes-devtools/gcc/gcc-${PV}.inc
<<<<<<< HEAD
require gcc-cross.inc

=======
require gcc-cross4.inc

EXTRA_OECONF += "--disable-libunwind-exceptions \
                 --with-mpfr=${STAGING_DIR_NATIVE}${prefix_native} \
                 --with-system-zlib "

EXTRA_OECONF_PATHS = " \
                      --with-gxx-include-dir=${STAGING_DIR_TARGET}${target_includedir}/c++ \
                      --with-sysroot=${STAGING_DIR_TARGET} \
                      --with-build-sysroot=${STAGING_DIR_TARGET}"


ARCH_FLAGS_FOR_TARGET += "-isystem${STAGING_DIR_TARGET}${target_includedir}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
