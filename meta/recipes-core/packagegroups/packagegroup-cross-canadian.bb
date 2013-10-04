SUMMARY = "Host SDK package for cross canadian toolchain"
<<<<<<< HEAD
PN = "packagegroup-cross-canadian-${MACHINE}"
PR = "r0"
LICENSE = "MIT"

# Save TRANSLATED_TARGET_ARCH before allarch tramples it
TRANSLATED_TARGET_ARCH = "${@d.getVar('TUNE_ARCH', True).replace('_', '-')}"

=======
PN = "packagegroup-cross-canadian-${TRANSLATED_TARGET_ARCH}"
PR = "r0"
LICENSE = "MIT"

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
inherit cross-canadian packagegroup

PACKAGEGROUP_DISABLE_COMPLEMENTARY = "1"

<<<<<<< HEAD
RDEPENDS_${PN} = "\
    binutils-cross-canadian-${@' binutils-cross-canadian-'.join(all_multilib_tune_values(d,'TRANSLATED_TARGET_ARCH').split())} \
    gdb-cross-canadian-${@' gdb-cross-canadian-'.join(all_multilib_tune_values(d, 'TRANSLATED_TARGET_ARCH').split())} \
    gcc-cross-canadian-${@' gcc-cross-canadian-'.join(all_multilib_tune_values(d, 'TRANSLATED_TARGET_ARCH').split())} \
    meta-environment-${MACHINE} \
=======
# For backwards compatibility after rename
RPROVIDES_${PN} = "task-cross-canadian-${TRANSLATED_TARGET_ARCH}"

RDEPENDS_${PN} = "\
    binutils-cross-canadian-${TRANSLATED_TARGET_ARCH} \
    gdb-cross-canadian-${TRANSLATED_TARGET_ARCH} \
    gcc-cross-canadian-${TRANSLATED_TARGET_ARCH} \
    meta-environment-${TRANSLATED_TARGET_ARCH} \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    "

