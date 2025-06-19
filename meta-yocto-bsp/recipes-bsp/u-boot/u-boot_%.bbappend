FILESEXTRAPATHS:prepend := "${THISDIR}/u-boot/${MACHINE}:"

# Add the configuration for libubootenv to the u-boot-env package
SRC_URI:append:beaglebone-yocto = " file://fw_env.config"
