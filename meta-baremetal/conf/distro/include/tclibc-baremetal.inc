#
# baremetal configuration
#

LIBCEXTENSION = ""

# Add baremetal libc overrides to the overrides.
LIBCOVERRIDE = ":libc-baremetal"
OVERRIDES .= "${LIBCOVERRIDE}"

ASSUME_PROVIDED += "virtual/libc virtual/libiconv"

PREFERRED_PROVIDER_virtual/libc ?= "musl"
PREFERRED_PROVIDER_virtual/libiconv ?= "musl"
PREFERRED_PROVIDER_virtual/libintl ?= "gettext"
PREFERRED_PROVIDER_virtual/nativesdk-libintl ?= "nativesdk-eglibc"
PREFERRED_PROVIDER_virtual/nativesdk-libiconv ?= "nativesdk-eglibc"

USE_NLS ?= "no"
IMAGE_LINGUAS = ""
LIBC_DEPENDENCIES = ""

# Doesn't work due to overrides issues
#DEPENDS_remove_pn-gcc-cross-${TARGET_ARCH} = "virtual/${TARGET_PREFIX}libc-for-gcc"
#EXTRA_OECONF_pn-gcc-cross-${TARGET_ARCH}_append = " --without-headers"

DEPENDS_remove_pn-meta-toolchain = "virtual/libc virtual/${TARGET_PREFIX}compilerlibs"

TARGET_OS = "elf"
TARGET_OS_arm = "eabi"

TOOLCHAIN_HOST_TASK ?= "nativesdk-packagegroup-sdk-host packagegroup-cross-canadian-${MACHINE}"
#TOOLCHAIN_HOST_TASK ?= "packagegroup-cross-canadian-${MACHINE}"
TOOLCHAIN_HOST_TASK_ATTEMPTONLY ?= ""
TOOLCHAIN_TARGET_TASK ?= "libgcc-dev"
TOOLCHAIN_NEED_CONFIGSITE_CACHE_remove = "${TCLIBC} zlib ncurses"
