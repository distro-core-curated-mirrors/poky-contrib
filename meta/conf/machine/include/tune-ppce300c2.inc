DEFAULTTUNE ?= "ppce300c2"

require conf/machine/include/powerpc/arch-powerpc.inc

TUNEVALID[ppce300c2] = "Enable ppce300c2 specific processor optimizations"
<<<<<<< HEAD
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "ppce300c2", " -mcpu=e300c2", "", d)}"
=======
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "ppce300c2", "-mcpu=e300c2", "", d)}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

AVAILTUNES += "ppce300c2"
TUNE_FEATURES_tune-ppce300c2 = "m32 fpu-soft ppce300c2"
TUNE_PKGARCH_tune-ppce300c2 = "ppce300c2"
PACKAGE_EXTRA_ARCHS_tune-ppce300c2 = "${PACKAGE_EXTRA_ARCHS_tune-powerpc-nf} ppce300c2"
