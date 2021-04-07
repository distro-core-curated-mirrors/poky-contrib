SUMMARY = "Test Anything Protocol (TAP) reporting plugin for nose"
HOMEPAGE = "https://github.com/python-tap/nose-tap"
# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
#
# The following license files were not able to be identified and are
# represented as "Unknown" below, you will need to check them yourself:
#   LICENSE
LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://LICENSE;md5=6fca73288e1ed8c09e87d340d54655e5"

SRC_URI[sha256sum] = "d4f174e6f778ecac0327323f7a0a52441ba1ce49e665fac9307abf9199f7b57d"
SRC_URI[sha384sum] = "ddb8643c2481a211f048891f7ff317e00e641b8a9539a35713af7c71eddd78327580409c45508f354d529df9466e149b"
SRC_URI[sha512sum] = "669040d1e1574ddcf11f29868e7c36b54eb463b3b9949f57e60ce74916a706fc0953457148367c5e251f48ae31942d8f764a9a5955ad2a91925b3199c1e6cae1"

S = "${WORKDIR}/nose-tap-${PV}"

inherit pypi setuptools3

RDEPENDS_${PN} += "python3-nose python3-tap-py"
RDEPENDS_${PN}-class-target += "python3-unittest"

# WARNING: We were unable to map the following python package/module
# dependencies to the bitbake packages which include them:
#    gettext
#    nose.plugins
#    nose.suite
#    os
#    tap
#    tap.tracker
#    unittest

BBCLASSEXTEND = "native nativesdk"
