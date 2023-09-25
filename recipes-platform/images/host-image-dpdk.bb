SUMMARY = "dpdk demo image"
LICENSE = "MIT"

require lxc-host-image-minimal.bb

CONTAINER_IMAGES ?= "agl-container-dpdk:guest-image-dpdk-demo"

IMAGE_INSTALL:append = " \
    kernel-modules \
"

# packages required for network bridge settings via lxc-net
IMAGE_INSTALL:append = " \
    lxc \
    iptables-modules \
    dnsmasq \
    systemd-netif-config \
    dpdk \
    dpdk-tools \
    dpdk-examples \
"
IMAGE_ROOTFS_EXTRA_SPACE = "8000000"
COMPATIBLE_MACHINE:pn-dpdk = "qemux86-64"
COMPATIBLE_MACHINE:pn-dpdk-module = "qemux86-64"

# Replace busybox
PREFERRED_PROVIDER_virtual/base-utils = "coreutils"
VIRTUAL-RUNTIME_base-utils = "coreutils"
VIRTUAL-RUNTIME_base-utils-hwclock = "util-linux-hwclock"
VIRTUAL-RUNTIME_base-utils-syslog = ""

# network manager to use
VIRTUAL-RUNTIME_net_manager = "systemd"

QB_MEM = "-m 12288"
DISTRO_FEATURES:append = ' systemd usrmerge '
VIRTUAL-RUNTIME_init_manager = "systemd"
VIRTUAL-RUNTIME_initscript = "systemd-compat-units"
