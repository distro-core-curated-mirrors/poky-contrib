require conf/machine/include/ia32/arch-ia32.inc

TUNEVALID[c3] = "VIA Cyrix III or VIA C3 specific optimizations"
TUNECONFLICTS[c3] = "m64 mx32"
<<<<<<< HEAD
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "c3", " -march=c3 -mtune=c3", "", d)}"
=======
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "c3", "-march=c3 -mtune=c3", "", d)}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

AVAILTUNES += "c3"
TUNE_FEATURES_tune-c3 = "${TUNE_FEATURES_tune-x86} c3"
BASE_LIBS_tune-c3 = "${BASE_LIB_tune-x86}"
# The following should likely be something other then i586...
TUNE_PKGARCH_tune-c3 = "i586"
PACKAGE_EXTRA_ARCHS_tune-c3 = "${PACKAGE_EXTRA_ARCHS_tune-x86} i386 i486 i586"
