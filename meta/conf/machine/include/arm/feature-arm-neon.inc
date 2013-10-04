TUNEVALID[neon] = "Enable Neon SIMD accelerator unit."
<<<<<<< HEAD
TUNE_CCARGS .= "${@bb.utils.contains("TUNE_FEATURES", "neon", " -mfpu=neon", "" ,d)}"
=======
TUNE_CCARGS += "${@bb.utils.contains("TUNE_FEATURES", "neon", "-mfpu=neon", "" ,d)}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
ARMPKGSFX_FPU .= "${@bb.utils.contains("TUNE_FEATURES", "neon", "-neon", "" ,d)}"
