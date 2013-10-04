DEFAULTTUNE ?= "cortexm3"
<<<<<<< HEAD
=======
ARMPKGARCH ?= "armv7m"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

require conf/machine/include/arm/arch-armv7a.inc

TUNEVALID[cortexm3] = "Enable Cortex-M3 specific processor optimizations"
<<<<<<< HEAD
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "cortexm3", " -mtune=cortex-m3", "", d)}"

TUNEVALID[armv7m] = "Enable Cortex-M3 specific processor optimizations"
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "armv7m", " -march=armv7-m", "", d)}"

AVAILTUNES += "cortexm3"
ARMPKGARCH_tune-cortexm3 = "armv7m"
TUNE_FEATURES_tune-cortexm3 = "armv7m vfp cortexm3"
PACKAGE_EXTRA_ARCHS_tune-cortexm3 = "${PACKAGE_EXTRA_ARCHS_tune-armv7at} armv7m-vfp"
=======
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "cortexm3", "-mtune=cortex-m3", "", d)}"

TUNEVALID[armv7m] = "Enable Cortex-M3 specific processor optimizations"
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "armv7m", "-march=armv7-m", "", d)}"

AVAILTUNES += "cortexm3"
TUNE_FEATURES_tune-cortexm3 = "armv7m vfp cortexm3"
PACKAGE_EXTRA_ARCHS_tune-cortexm3 = "${PACKAGE_EXTRA_ARCHS_tune-armv7at} armv7m-vfp"

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
