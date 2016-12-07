# meta-environment for extensible SDK

require meta-environment.bb

PN = "meta-environment-extsdk-${MACHINE}"

create_sdk_files_append() {
	local sysroot=${SDKPATH}/${@os.path.relpath(d.getVar('STAGING_DIR'), d.getVar('TOPDIR'))}/${MACHINE}
	local sdkpathnative=${SDKPATH}/${@os.path.relpath(d.getVar('STAGING_DIR'), d.getVar('TOPDIR'))}/${BUILD_ARCH}

	toolchain_create_sdk_env_script '' '' $sysroot '' ${bindir_native} ${prefix_native} $sdkpathnative
}
