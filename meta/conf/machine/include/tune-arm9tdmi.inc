<<<<<<< HEAD
DEFAULTTUNE ?= "armv4t"
=======
DEFAULTTUNE ?= "arm9tdmi"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

require conf/machine/include/arm/arch-armv4.inc

TUNEVALID[arm9tdmi] = "Enable arm9tdmi specific processor optimizations"
<<<<<<< HEAD
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "arm9tdmi", " -mtune=arm9tdmi", "", d)}"

AVAILTUNES += "arm9tdmi"
ARMPKGARCH_tune-arm9tdmi = "arm9tdmi"
TUNE_FEATURES_tune-arm9tdmi = "${TUNE_FEATURES_tune-armv4t} arm9tdmi"
PACKAGE_EXTRA_ARCHS_tune-arm9tdmi = "${PACKAGE_EXTRA_ARCHS_tune-armv4t} arm9tdmit"
=======
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "arm9tdmi", "-mtune=arm9tdmi", "", d)}"

AVAILTUNES += "arm9tdmi"
TUNE_FEATURES_tune-arm9tdmi = "${TUNE_FEATURES_tune-armv4t} arm9tdmi"
PACKAGE_EXTRA_ARCHS_tune-arm9tdmi = "${PACKAGE_EXTRA_ARCHS_tune-armv4t}"

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
