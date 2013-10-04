<<<<<<< HEAD
DEFAULTTUNE ?= "armv4t"
=======
DEFAULTTUNE ?= "arm920t"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

require conf/machine/include/arm/arch-armv4.inc

TUNEVALID[arm920t] = "Enable arm920t specific processor optimizations"
<<<<<<< HEAD
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "arm920t", " -mtune=arm920t", "", d)}"

AVAILTUNES += "arm920t"
ARMPKGARCH_tune-arm920t = "arm920t"
TUNE_FEATURES_tune-arm920t = "${TUNE_FEATURES_tune-armv4t} arm920t"
PACKAGE_EXTRA_ARCHS_tune-arm920t = "${PACKAGE_EXTRA_ARCHS_tune-armv4t} arm920tt"
=======
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "arm920t", "-mtune=arm920t", "", d)}"

AVAILTUNES += "arm920t"
TUNE_FEATURES_tune-arm920t = "${TUNE_FEATURES_tune-armv4t} arm920t"
PACKAGE_EXTRA_ARCHS_tune-arm920t = "${PACKAGE_EXTRA_ARCHS_tune-armv4t}"

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
