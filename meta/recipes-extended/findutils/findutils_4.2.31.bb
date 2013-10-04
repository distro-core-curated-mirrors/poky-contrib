LICENSE = "GPLv2+"
LIC_FILES_CHKSUM = "file://COPYING;md5=59530bdf33659b29e73d4adb9f9f6552"
PR = "r4"

require findutils.inc

SRC_URI += "file://gnulib-extension.patch \
            file://findutils_fix_for_automake-1.12.patch \
<<<<<<< HEAD
            file://findutils-fix-doc-build-error.patch \
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
           "

SRC_URI[md5sum] = "a0e31a0f18a49709bf5a449867c8049a"
SRC_URI[sha256sum] = "e0d34b8faca0b3cca0703f6c6b498afbe72f0ba16c35980c10ec9ef7724d6204"
