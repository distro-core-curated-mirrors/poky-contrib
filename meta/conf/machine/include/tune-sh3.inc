DEFAULTTUNE ?= "sh3"

require conf/machine/include/sh/arch-sh.inc

TUNEVALID[sh3] = "Enable SH3 optimizations"
<<<<<<< HEAD
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "sh3", " -m3", "", d)}"
=======
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "sh3", "-m3", "", d)}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

AVAILTUNES += "sh3 sh3eb"
TUNE_FEATURES_tune-sh3 = "sh3"
TUNE_ARCH_tune-sh3 = "sh3"
TUNE_PKGARCH_tune-sh3 = "sh3"
PACKAGE_EXTRA_ARCHS_tune-sh3 = "sh sh3"

TUNE_FEATURES_tune-sh3eb = "sh3 bigendian"
TUNE_ARCH_tune-sh3eb = "sh3eb"
TUNE_PKGARCH_tune-sh3eb = "sh3eb"
PACKAGE_EXTRA_ARCHS_tune-sh3eb = "sheb sh3eb"
