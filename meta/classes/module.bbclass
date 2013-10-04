<<<<<<< HEAD
=======
RDEPENDS_${PN} += "kernel-image ${@oe.utils.contains('DISTRO_FEATURES', 'update-modules', 'update-modules', '', d)}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
DEPENDS += "virtual/kernel"

inherit module-base kernel-module-split

addtask make_scripts after do_patch before do_compile
do_make_scripts[lockfiles] = "${TMPDIR}/kernel-scripts.lock"
do_make_scripts[deptask] = "do_populate_sysroot"

addtask make_scripts before do_compile
do_make_scripts[lockfiles] = "${TMPDIR}/kernel-scripts.lock"
do_make_scripts[deptask] = "do_populate_sysroot"

module_do_compile() {
	unset CFLAGS CPPFLAGS CXXFLAGS LDFLAGS
	oe_runmake KERNEL_PATH=${STAGING_KERNEL_DIR}   \
		   KERNEL_SRC=${STAGING_KERNEL_DIR}    \
		   KERNEL_VERSION=${KERNEL_VERSION}    \
		   CC="${KERNEL_CC}" LD="${KERNEL_LD}" \
		   AR="${KERNEL_AR}" \
		   ${MAKE_TARGETS}
}

module_do_install() {
	unset CFLAGS CPPFLAGS CXXFLAGS LDFLAGS
	oe_runmake DEPMOD=echo INSTALL_MOD_PATH="${D}" \
	           KERNEL_SRC=${STAGING_KERNEL_DIR} \
	           CC="${KERNEL_CC}" LD="${KERNEL_LD}" \
	           modules_install
<<<<<<< HEAD
=======
}

pkg_postinst_append () {
if [ -z "$D" ]; then
	depmod -a
	update-modules || true
fi
}

pkg_postrm_append () {
update-modules || true
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
}

EXPORT_FUNCTIONS do_compile do_install

# add all splitted modules to PN RDEPENDS, PN can be empty now
KERNEL_MODULES_META_PACKAGE = "${PN}"
FILES_${PN} = ""
ALLOW_EMPTY_${PN} = "1"
