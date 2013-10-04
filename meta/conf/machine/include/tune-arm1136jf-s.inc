<<<<<<< HEAD
DEFAULTTUNE ?= "armv6"
=======
DEFAULTTUNE ?= "arm1136jfs"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

require conf/machine/include/arm/arch-armv6.inc

TUNEVALID[arm1136jfs] = "Enable arm1136jfs specific processor optimizations"
<<<<<<< HEAD
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "arm1136jfs", " -mtune=arm1136jf-s", "", d)}"

AVAILTUNES += "arm1136jfs"
ARMPKGARCH_tune-arm1136jfs = "arm1136jfs"
TUNE_FEATURES_tune-arm1136jfs = "${TUNE_FEATURES_tune-armv6} arm1136jfs"
PACKAGE_EXTRA_ARCHS_tune-arm1136jfs = "${PACKAGE_EXTRA_ARCHS_tune-armv6} arm1136jfs-vfp"
=======
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "arm1136jfs", "-mtune=arm1136jf-s", "", d)}"

AVAILTUNES += "arm1136jfs"
TUNE_FEATURES_tune-arm1136jfs = "${TUNE_FEATURES_tune-armv6} arm1136jfs"
PACKAGE_EXTRA_ARCHS_tune-arm1136jfs = "${PACKAGE_EXTRA_ARCHS_tune-armv6}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
