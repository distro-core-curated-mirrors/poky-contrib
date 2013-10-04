<<<<<<< HEAD
DEFAULTTUNE ?= "armv5te"
=======
DEFAULTTUNE ?= "xscale"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

require conf/machine/include/arm/arch-armv5-dsp.inc

TUNEVALID[xscale] = "Enable PXA255/PXA26x Xscale specific processor optimizations"
<<<<<<< HEAD
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "xscale", " -mtune=xscale", "", d)}"

AVAILTUNES += "xscale"
ARMPKGARCH_tune-xscale = "xscale"
TUNE_FEATURES_tune-xscale = "${TUNE_FEATURES_tune-armv5te} xscale"
PACKAGE_EXTRA_ARCHS_tune-xscale = "${PACKAGE_EXTRA_ARCHS_tune-armv5te} xscale xscalet xscalee xscalete"

AVAILTUNES += "xscale-be"
ARMPKGARCH_tune-xscale-be = "xscale"
TUNE_FEATURES_tune-xscale-be = "${TUNE_FEATURES_tune-armv5teb} xscale bigendian"
PACKAGE_EXTRA_ARCHS_tune-xscale-be = "${PACKAGE_EXTRA_ARCHS_tune-armv5teb} xscaleb xscaletb xscaleeb xscaleteb"
=======
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "xscale", "-mtune=xscale", "", d)}"

AVAILTUNES += "xscale"
TUNE_FEATURES_tune-xscale = "${TUNE_FEATURES_tune-armv5te} xscale"
PACKAGE_EXTRA_ARCHS_tune-xscale = "${PACKAGE_EXTRA_ARCHS_tune-armv5te}"

AVAILTUNES += "xscale-be"
TUNE_FEATURES_tune-xscale-be = "${TUNE_FEATURES_tune-armv5teb} xscale bigendian"
PACKAGE_EXTRA_ARCHS_tune-xscale-be = "${PACKAGE_EXTRA_ARCHS_tune-armv5teb}"

# webkit-gtk has alignment issues with double instructions on armv5 so
# disable them here
TUNE_CCARGS_pn-webkit-gtk = "-march=armv4t"
TUNE_CCARGS_pn-cairo = "-march=armv4t"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
