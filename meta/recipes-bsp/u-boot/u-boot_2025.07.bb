require u-boot-common.inc
require u-boot.inc

DEPENDS += "bc-native dtc-native gnutls-native python3-pyelftools-native"

# workarounds for aarch64 kvm qemu boot regressions
SRC_URI:append:qemuarm64 = " file://disable-CONFIG_BLOBLIST.cfg"
SRC_URI:append:genericarm64 = " file://disable-CONFIG_BLOBLIST.cfg"

SRC_URI = "git://source.denx.de/u-boot/u-boot.git;protocol=https;branch=master"
SRCREV = "34820924edbc4ec7803eb89d9852f4b870fa760a"


PKGV = "${PV}+${@get_pkgv(d)}-test"
UBOOT_VERSION = "${PKGV}-${PKGR}"

def get_pkgv(d):
    # BB_HASH_CODEPARSER_VALS sets SRC_URI to "" so if we see that, it means we're 
    # being expanded for dependencies only and can just return a dummy value
    if not d.getVar("SRC_URI"):
        return ""
    return bb.fetch2.get_srcrev(d, 'gitpkgv_revision')
