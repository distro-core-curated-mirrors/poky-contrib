SUMMARY = "File type identification using libmagic"
HOMEPAGE = "http://github.com/ahupp/python-magic"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=16a934f165e8c3245f241e77d401bb88"

SRC_URI = "git://github.com/ahupp/python-magic.git;protocol=https"

PV = "0.4.12+git${SRCPV}"
SRCREV = "37cb2271dd472771b18e141c949a93c4b64d8612"

DEPENDS_${PN} += "file"
DEPENDS_class-native += "file-native"

S = "${WORKDIR}/git"

BBCLASSEXTEND = "native"
