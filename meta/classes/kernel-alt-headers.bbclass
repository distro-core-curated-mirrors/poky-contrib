PACKAGE_ARCH = "${MACHINE_ARCH}"

#
# Provide alternate uapi headers from a kernel, for use by
# a recipe. This is *not* a replacement for the linux-libc-headers
# package, but is expected to be used when a package is tightly
# coupled to a specific kernel and needs definitions / interfaces
# specific to that kernel.
#
# The class works in one of two ways, it can be included by the
# recipe that requires the headers (mode 1 below) or by a kernel
# recipe that provides the alternate headers. Both are valid,
# and one may be chosen over the other depending on how many
# packages need custom headers, etc.
#
# It is up to the package that builds against these headers to
# ensure that the alternate kernel headers are in the include
# path and used for the build.
#
# mode 1: included directly from a recipe that needs alternate
#         kernel headers. In this mode the headers install from
#         the shared kernel dir to WORKDIR.
#         Note: in this mode, the kernel doesn't (or shouldn't)
#               inherit kernel-alt-headers itself.
#
#         The headers will be in: $WORKDIR/usr/alt-headers
#
# mode 2: included by a kernel recipe to provide alt-headers.
#         In this mode, the kernel build/install is modified to
#         stage the headers to the sysroot (and create a
#         kernel-headers-alt package).
#
#         The headers are found in: recipe-sysroot/usr/alt-headers
#
inherit kernel-arch

KERNEL_ALT_HEADER_DIR ?= "/usr/alt-headers/"
DEPENDS += "unifdef-native bison-native rsync-native"

KERNEL_SOURCE_IS_LOCAL ?= "${@(bb.data.inherits_class('kernel', d))}"
python __anonymous () {
    if not bb.data.inherits_class('kernel',d):
        d.appendVar( 'DEPENDS', " virtual/kernel" )
    else:
        # We need to package these up, even if they aren't expected to be
        # used for anything
        d.appendVar( 'PACKAGES', " ${KERNEL_PACKAGE_NAME}-headers-alt" )
        d.setVar( 'FILES:${KERNEL_PACKAGE_NAME}-headers-alt', "${KERNEL_ALT_HEADER_DIR}" )
}

do_compile:prepend() {
	if [ "${KERNEL_SOURCE_IS_LOCAL}" = "False" ]; then
		# install from the staging kernel directory
	    	oe_runmake -C ${STAGING_KERNEL_DIR} headers_install INSTALL_HDR_PATH=${WORKDIR}/${KERNEL_ALT_HEADER_DIR}
	    	# there have been reports that menuconfig won't run due to a dirty
		# kernel directory after the install, so we run mrproper to make sure
		# it is clean
		oe_runmake -C ${STAGING_KERNEL_DIR} mrproper
	fi
}

do_install:append() {
    	if [ "${KERNEL_SOURCE_IS_LOCAL}" = "True" ]; then
	   	# install to our deploy directory, this will be packaged and staged
		oe_runmake headers_install INSTALL_HDR_PATH=${D}${KERNEL_ALT_HEADER_DIR}

		# remove export artifacts
		find ${D}${KERNEL_ALT_HEADER_DIR} -name .install -exec rm {} \;
		find ${D}${KERNEL_ALT_HEADER_DIR} -name ..install.cmd -exec rm {} \;
	fi
}

sysroot_stage_all:append() {
	if [ "${KERNEL_SOURCE_IS_LOCAL}" = "True" ]; then
		mkdir -p ${SYSROOT_DESTDIR}${KERNEL_ALT_HEADER_DIR}
		cp -r ${D}${KERNEL_ALT_HEADER_DIR}/* ${SYSROOT_DESTDIR}/${KERNEL_ALT_HEADER_DIR}
	fi
}
