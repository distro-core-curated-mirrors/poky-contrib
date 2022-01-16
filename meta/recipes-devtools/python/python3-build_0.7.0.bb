SUMMARY = "A simple, correct PEP517 package builder"
HOMEPAGE = "UNKNOWN"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=310439af287b0fb4780b2ad6907c256c"

SRC_URI[sha256sum] = "1aaadcd69338252ade4f7ec1265e1a19184bf916d84c9b7df095f423948cb89f"

inherit pypi setuptools3

RDEPENDS:${PN} += "python3-core"

BBCLASSEXTEND = "native nativesdk"
