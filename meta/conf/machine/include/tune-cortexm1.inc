<<<<<<< HEAD
DEFAULTTUNE ?= "armv7a"
=======
DEFAULTTUNE ?= "cortexm1"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

require conf/machine/include/arm/arch-armv7a.inc

TUNEVALID[cortexm1] = "Enable Cortex-M1 specific processor optimizations"
<<<<<<< HEAD
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "cortexm1", " -mtune=cortex-m1", "", d)}"

AVAILTUNES += "cortexm1"
ARMPKGARCH_tune-cortexm1 = "cortexm1"
TUNE_FEATURES_tune-cortexm1 = "${TUNE_FEATURES_tune-armv7a} cortexm1"
PACKAGE_EXTRA_ARCHS_tune-cortexm1 = "${PACKAGE_EXTRA_ARCHS_tune-armv7at} cortexm1-vfp"
=======
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "cortexm1", "-mtune=cortex-m1", "", d)}"

AVAILTUNES += "cortexm1"
TUNE_FEATURES_tune-cortexm1 = "${TUNE_FEATURES_tune-armv7a} cortexm1"
PACKAGE_EXTRA_ARCHS_tune-cortexm1 = "${PACKAGE_EXTRA_ARCHS_tune-armv7at}"

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
