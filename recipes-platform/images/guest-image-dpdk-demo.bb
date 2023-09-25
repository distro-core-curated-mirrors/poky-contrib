SUMMARY = "dpdk guest image"
LICENSE = "MIT"

require guest-image-minimal.bb

IMAGE_INSTALL += " \
    dpdk \
    dpdk-tools \
    dpdk-examples \
    spice-guest-vdagent \
"
