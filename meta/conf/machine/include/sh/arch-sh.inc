# SH Architecture definition

DEFAULTTUNE ?= "sh"

TUNE_ARCH = "${TUNE_ARCH_tune-${DEFAULTTUNE}}"
TUNE_PKGARCH = "${TUNE_PKGARCH_tune-${DEFAULTTUNE}}"

TUNEVALID[bigendian] = "Enabled big-endian mode."
<<<<<<< HEAD
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "bigendian", " -mb", " -ml", d)}"
=======
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "bigendian", "-mb", "-ml", d)}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
