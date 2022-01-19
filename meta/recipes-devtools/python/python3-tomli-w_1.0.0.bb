LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=aaaaf0879d17df0110d1aa8c8c9f46f5"

SRC_URI[sha256sum] = "f463434305e0336248cac9c2dc8076b707d8a12d019dd349f5c1e382dd1ae1b9"

PYPI_PACKAGE = "tomli_w"

inherit pypi flit_core

BBCLASSEXTEND = "native nativesdk"
