DEFAULTTUNE ?= "ep9312"
<<<<<<< HEAD

require conf/machine/include/arm/arch-armv4.inc
=======
ARMPKGARCH ?= "ep9312"

require conf/machine/include/arm/arch-armv4.inc

TUNEVALID[ep9312] = "Enable Intel PXA27x specific processor optimizations"
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "ep9312", "-march=ep9312 -mtune=ep9312", "", d)}"

AVAILTUNES += "ep9312"
TUNE_FEATURES_tune-ep9312 = "thumb ep9312"
PACKAGE_EXTRA_ARCHS_tune-ep9312 = "${PACKAGE_EXTRA_ARCHS_tune-armv4t} ep9312"

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

TUNEVALID[ep9312] = "Enable Intel PXA27x specific processor optimizations"
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "ep9312", " -march=ep9312 -mtune=ep9312", "", d)}"

AVAILTUNES += "ep9312"
ARMPKGARCH_tune-ep9312 = "ep9312"
# this tune does not include TUNE_FEATURES_tune-armv4t, so there is no armv4 TUNE_FEATURES => no 't' in ARMPKGSFX_THUMB
TUNE_FEATURES_tune-ep9312 = "thumb ep9312"
PACKAGE_EXTRA_ARCHS_tune-ep9312 = "${PACKAGE_EXTRA_ARCHS_tune-armv4t} ep9312"
