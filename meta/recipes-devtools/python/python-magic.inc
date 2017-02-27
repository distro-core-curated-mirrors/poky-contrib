SUMMARY = "File type identification using libmagic"
HOMEPAGE = "http://github.com/ahupp/python-magic"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=16a934f165e8c3245f241e77d401bb88"

SRC_URI = "git://github.com/ahupp/python-magic.git;protocol=https"

UPSTREAM_CHECK_GITTAGREGEX = "(?P<pver>\d+(\.\d+)+)"

PV = "0.4.15+git${SRCPV}"
SRCREV = "a60800c1a614a2964985eb614f2aa9082f148edf"

S = "${WORKDIR}/git"

RDEPENDS_${PN} += "file"

BBCLASSEXTEND = "native"
