SUMMARY = "Jansson is a C library for encoding, decoding and manipulating JSON data"
SECTION = "libs"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=8b70213ec164c7bd876ec2120ba52f61"

SRC_URI = "git://github.com/akheron/jansson.git \
"

SRCREV = "b23201bb1a566d7e4ea84b76b3dcf2efcc025dac"

S = "${WORKDIR}/git"

inherit autotools pkgconfig

FILES_${PN} += "${libdir}/libjansson.so.* \
"
FILES_${PN}-dev += "${includedir}/jansson.h \
                    ${includedir}/jansson_config.h \
                    ${libdir}/libjansson.so \
                    ${libdir}/libjansson.la \
"

