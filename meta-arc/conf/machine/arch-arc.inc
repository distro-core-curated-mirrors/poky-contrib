DEFAULTTUNE ?= "arc"

TUNE_ARCH = "arc"
TUNE_PKGARCH = "arc"
TUNE_FEATURES_tune-arc = "bigendian"
TUNE_CCARGS = "-mARCv2EM -mav2em"

TUNEVALID[bigendian] = "Big endian mode"
