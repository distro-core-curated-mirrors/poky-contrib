SUMMARY = "Device Tree Compiler"
DESCRIPTION = "The Device Tree Compiler is a tool used to manipulate the Open-Firmware-like device tree used by PowerPC kernels."
SECTION = "bootloader"
LICENSE = "GPLv2 | BSD"
DEPENDS = "flex-native bison-native"

inherit autotools

<<<<<<< HEAD
SRC_URI = "git://www.jdl.com/software/dtc.git \
=======
SRC_URI = "git://www.jdl.com/software/dtc.git;protocol=git \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
           file://make_install.patch \
	  "

EXTRA_OEMAKE='PREFIX="${prefix}" LIBDIR="${libdir}"'
<<<<<<< HEAD
=======
INC_PR = "r3"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

S = "${WORKDIR}/git"

PACKAGES =+ "${PN}-misc"
FILES_${PN}-misc = "${bindir}/convert-dtsv0 ${bindir}/ftdump ${bindir}/dtdiff"
