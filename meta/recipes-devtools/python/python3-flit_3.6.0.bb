LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=41eb78fa8a872983a882c694a8305f08"

SRC_URI[sha256sum] = "b1464e006df4df4c8eeb37671c0e0ce66e1d04e4a36d91b702f180a25fde3c11"

inherit flit_core pypi

DEPENDS += "python3 python3-pip-native"

RDEPENDS_${PN} += "python3-docutils python3-flit-core python3-requests python3-tomli python3-tomli-w"

BBCLASSEXTEND = "native nativesdk"

