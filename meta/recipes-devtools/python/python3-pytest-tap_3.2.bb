SUMMARY = "Test Anything Protocol (TAP) reporting plugin for pytest"
HOMEPAGE = "https://github.com/python-tap/pytest-tap"
# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
#
# The following license files were not able to be identified and are
# represented as "Unknown" below, you will need to check them yourself:
#   LICENSE
LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://LICENSE;md5=6fca73288e1ed8c09e87d340d54655e5"

SRC_URI[sha256sum] = "1b585c4a636458dbd958d136381bbabb1752c5877d05fac7d6a6001a8a9ddc29"
SRC_URI[sha384sum] = "d48e0b310b546400b5abd3ad91e4ee313f54456b8d4ee654c727eb08381f15b6ee39adef360b532a32148a0fb3bb6ead"
SRC_URI[sha512sum] = "59a35005cc10a719d1e1fff2e10f8adb639f5e5c7867a9a7c19608d87b8b7a13659f0280a838d8059253be4652e800b6eb9994bbc7bc79a98f4d1a176355ce3a"

S = "${WORKDIR}/pytest-tap-${PV}"

inherit pypi setuptools3

RDEPENDS_${PN} += "python3-pytest python3-tap-py"

BBCLASSEXTEND = "native nativesdk"
