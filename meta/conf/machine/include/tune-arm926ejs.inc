<<<<<<< HEAD
DEFAULTTUNE ?= "armv5te"
=======
DEFAULTTUNE ?= "arm926ejs"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

require conf/machine/include/arm/arch-armv5-dsp.inc

TUNEVALID[arm926ejs] = "Enable arm926ejs specific processor optimizations"
<<<<<<< HEAD
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "arm926ejs", " -mtune=arm926ej-s", "", d)}"

AVAILTUNES += "arm926ejs"
ARMPKGARCH_tune-arm926ejs = "arm926ejs"
TUNE_FEATURES_tune-arm926ejs = "${TUNE_FEATURES_tune-armv5te} arm926ejs"
PACKAGE_EXTRA_ARCHS_tune-arm926ejs = "${PACKAGE_EXTRA_ARCHS_tune-armv5te} arm926ejste"
=======
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "arm926ejs", "-mtune=arm926ej-s", "", d)}"

AVAILTUNES += "arm926ejs"
TUNE_FEATURES_tune-arm926ejs = "${TUNE_FEATURES_tune-armv5te} arm926ejs"
PACKAGE_EXTRA_ARCHS_tune-arm926ejs = "${PACKAGE_EXTRA_ARCHS_tune-armv5te}"

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
