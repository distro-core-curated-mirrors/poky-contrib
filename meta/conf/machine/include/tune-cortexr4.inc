DEFAULTTUNE ?= "cortexr4"
<<<<<<< HEAD
=======
ARMPKGARCH ?= "armv7r"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

require conf/machine/include/arm/arch-armv7a.inc

TUNEVALID[cortexr4] = "Enable Cortex-R4 specific processor optimizations"
<<<<<<< HEAD
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "cortexr4", " -mtune=cortex-r4", "", d)}"

TUNEVALID[armv7r] = "Enable Cortex-R4 specific processor optimizations"
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "armv7r", " -march=armv7-r", "", d)}"

AVAILTUNES += "cortexr4"
ARMPKGARCH_tune-cortexr4 = "armv7r"
=======
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "cortexr4", "-mtune=cortex-r4", "", d)}"

TUNEVALID[armv7r] = "Enable Cortex-R4 specific processor optimizations"
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "armv7r", "-march=armv7-m", "", d)}"

AVAILTUNES += "cortexr4"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
TUNE_FEATURES_tune-cortexr4 = "armv7r vfp cortexr4"
PACKAGE_EXTRA_ARCHS_tune-cortexr4 = "${PACKAGE_EXTRA_ARCHS_tune-armv7at} armv7r-vfp"
