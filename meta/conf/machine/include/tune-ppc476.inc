DEFAULTTUNE ?= "ppc476"

require conf/machine/include/powerpc/arch-powerpc.inc

TUNEVALID[ppc476] = "Enable ppc476 specific processor optimizations"
<<<<<<< HEAD
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "ppc476", " -mcpu=476", "", d)}"
=======
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "ppc476", "-mcpu=476", "", d)}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

AVAILTUNES += "ppc476"
TUNE_FEATURES_tune-ppc476 = "m32 fpu-hard ppc476"
TUNE_PKGARCH_tune-ppc476 = "ppc476"
PACKAGE_EXTRA_ARCHS_tune-ppc476 = "${PACKAGE_EXTRA_ARCHS_tune-powerpc} ppc476"

# glibc configure options to get 476 specific library (for sqrt)
GLIBC_EXTRA_OECONF += "${@bb.utils.contains("TUNE_FEATURES", "ppc476", "-with-cpu=476", "", d)}"
