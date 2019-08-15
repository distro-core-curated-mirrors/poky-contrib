BUILDHISTORY_DIR_SDK = "${BUILDHISTORY_DIR}/sdk/${SDK_NAME}${SDK_EXT}/${IMAGE_BASENAME}"
BUILDHISTORY_SDK_FILES ?= "conf/local.conf conf/bblayers.conf conf/auto.conf conf/locked-sigs.inc conf/devtool.conf"

# We want these to be the last run so that we get called after complementary package installation
POPULATE_SDK_POST_TARGET_COMMAND_append = " buildhistory_list_installed_sdk_target;"
POPULATE_SDK_POST_TARGET_COMMAND_append = " buildhistory_get_sdk_installed_target;"
POPULATE_SDK_POST_TARGET_COMMAND[vardepvalueexclude] .= "| buildhistory_list_installed_sdk_target;| buildhistory_get_sdk_installed_target;"

POPULATE_SDK_POST_HOST_COMMAND_append = " buildhistory_list_installed_sdk_host;"
POPULATE_SDK_POST_HOST_COMMAND_append = " buildhistory_get_sdk_installed_host;"
POPULATE_SDK_POST_HOST_COMMAND[vardepvalueexclude] .= "| buildhistory_list_installed_sdk_host;| buildhistory_get_sdk_installed_host;"

SDK_POSTPROCESS_COMMAND_append = " buildhistory_get_sdkinfo ; buildhistory_get_extra_sdkinfo; "
SDK_POSTPROCESS_COMMAND[vardepvalueexclude] .= "| buildhistory_get_sdkinfo ; buildhistory_get_extra_sdkinfo; "

buildhistory_get_sdk_installed() {
	# Anything requiring the use of the packaging system should be done in here
	# in case the packaging files are going to be removed for this SDK

	if [ "${@bb.utils.contains('BUILDHISTORY_FEATURES', 'sdk', '1', '0', d)}" = "0" ] ; then
		return
	fi

	buildhistory_get_installed ${BUILDHISTORY_DIR_SDK}/$1 sdk
}

buildhistory_get_sdkinfo() {
	if [ "${@bb.utils.contains('BUILDHISTORY_FEATURES', 'sdk', '1', '0', d)}" = "0" ] ; then
		return
	fi

	buildhistory_list_files ${SDK_OUTPUT} ${BUILDHISTORY_DIR_SDK}/files-in-sdk.txt

	# Collect files requested in BUILDHISTORY_SDK_FILES
	rm -rf ${BUILDHISTORY_DIR_SDK}/sdk-files
	for f in ${BUILDHISTORY_SDK_FILES}; do
		if [ -f ${SDK_OUTPUT}/${SDKPATH}/$f ] ; then
			mkdir -p ${BUILDHISTORY_DIR_SDK}/sdk-files/`dirname $f`
			cp ${SDK_OUTPUT}/${SDKPATH}/$f ${BUILDHISTORY_DIR_SDK}/sdk-files/$f
		fi
	done

	# Record some machine-readable meta-information about the SDK
	printf ""  > ${BUILDHISTORY_DIR_SDK}/sdk-info.txt
	cat >> ${BUILDHISTORY_DIR_SDK}/sdk-info.txt <<END
${@buildhistory_get_sdkvars(d)}
END
	sdksize=`du -ks ${SDK_OUTPUT} | awk '{ print $1 }'`
	echo "SDKSIZE = $sdksize" >> ${BUILDHISTORY_DIR_SDK}/sdk-info.txt
}

python buildhistory_list_installed_sdk_target() {
    buildhistory_list_installed(d, "sdk_target")
}

python buildhistory_list_installed_sdk_host() {
    buildhistory_list_installed(d, "sdk_host")
}

buildhistory_get_sdk_installed_host() {
	buildhistory_get_sdk_installed host
}

buildhistory_get_sdk_installed_target() {
	buildhistory_get_sdk_installed target
}

python buildhistory_get_extra_sdkinfo() {
    import operator
    from oe.sdk import get_extra_sdkinfo

    sstate_dir = d.expand('${SDK_OUTPUT}/${SDKPATH}/sstate-cache')
    extra_info = get_extra_sdkinfo(sstate_dir)

    if d.getVar('BB_CURRENTTASK') == 'populate_sdk_ext' and \
            "sdk" in (d.getVar('BUILDHISTORY_FEATURES') or "").split():
        with open(d.expand('${BUILDHISTORY_DIR_SDK}/sstate-package-sizes.txt'), 'w') as f:
            filesizes_sorted = sorted(extra_info['filesizes'].items(), key=operator.itemgetter(1, 0), reverse=True)
            for fn, size in filesizes_sorted:
                f.write('%10d KiB %s\n' % (size, fn))
        with open(d.expand('${BUILDHISTORY_DIR_SDK}/sstate-task-sizes.txt'), 'w') as f:
            tasksizes_sorted = sorted(extra_info['tasksizes'].items(), key=operator.itemgetter(1, 0), reverse=True)
            for task, size in tasksizes_sorted:
                f.write('%10d KiB %s\n' % (size, task))
}

def buildhistory_get_sdkvars(d):
    if d.getVar('BB_WORKERCONTEXT') != '1':
        return ""
    sdkvars = "DISTRO DISTRO_VERSION SDK_NAME SDK_VERSION SDKMACHINE SDKIMAGE_FEATURES BAD_RECOMMENDATIONS NO_RECOMMENDATIONS PACKAGE_EXCLUDE"
    if d.getVar('BB_CURRENTTASK') == 'populate_sdk_ext':
        # Extensible SDK uses some additional variables
        sdkvars += " SDK_LOCAL_CONF_WHITELIST SDK_LOCAL_CONF_BLACKLIST SDK_INHERIT_BLACKLIST SDK_UPDATE_URL SDK_EXT_TYPE SDK_RECRDEP_TASKS SDK_INCLUDE_PKGDATA SDK_INCLUDE_TOOLCHAIN"
    listvars = "SDKIMAGE_FEATURES BAD_RECOMMENDATIONS PACKAGE_EXCLUDE SDK_LOCAL_CONF_WHITELIST SDK_LOCAL_CONF_BLACKLIST SDK_INHERIT_BLACKLIST"
    return outputvars(sdkvars, listvars, d)


