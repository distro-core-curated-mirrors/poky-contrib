BUILDHISTORY_DIR_IMAGE = "${BUILDHISTORY_DIR}/images/${MACHINE_ARCH}/${TCLIBC}/${IMAGE_BASENAME}"
BUILDHISTORY_IMAGE_FILES ?= "/etc/passwd /etc/group"

# By using ROOTFS_POSTUNINSTALL_COMMAND we get in after uninstallation of
# unneeded packages but before the removal of packaging files
ROOTFS_POSTUNINSTALL_COMMAND += "buildhistory_list_installed_image ;"
ROOTFS_POSTUNINSTALL_COMMAND += "buildhistory_get_image_installed ;"
ROOTFS_POSTUNINSTALL_COMMAND[vardepvalueexclude] .= "| buildhistory_list_installed_image ;| buildhistory_get_image_installed ;"
ROOTFS_POSTUNINSTALL_COMMAND[vardepsexclude] += "buildhistory_list_installed_image buildhistory_get_image_installed"

IMAGE_POSTPROCESS_COMMAND += "buildhistory_get_imageinfo ;"
IMAGE_POSTPROCESS_COMMAND[vardepvalueexclude] .= "| buildhistory_get_imageinfo ;"
IMAGE_POSTPROCESS_COMMAND[vardepsexclude] += "buildhistory_get_imageinfo"

python buildhistory_list_installed_image() {
    buildhistory_list_installed(d)
}

buildhistory_get_image_installed() {
	# Anything requiring the use of the packaging system should be done in here
	# in case the packaging files are going to be removed for this image

	if [ "${@bb.utils.contains('BUILDHISTORY_FEATURES', 'image', '1', '0', d)}" = "0" ] ; then
		return
	fi

	buildhistory_get_installed ${BUILDHISTORY_DIR_IMAGE}
}

buildhistory_get_imageinfo() {
	if [ "${@bb.utils.contains('BUILDHISTORY_FEATURES', 'image', '1', '0', d)}" = "0" ] ; then
		return
	fi

        mkdir -p ${BUILDHISTORY_DIR_IMAGE}
	buildhistory_list_files ${IMAGE_ROOTFS} ${BUILDHISTORY_DIR_IMAGE}/files-in-image.txt

	# Collect files requested in BUILDHISTORY_IMAGE_FILES
	rm -rf ${BUILDHISTORY_DIR_IMAGE}/image-files
	for f in ${BUILDHISTORY_IMAGE_FILES}; do
		if [ -f ${IMAGE_ROOTFS}/$f ] ; then
			mkdir -p ${BUILDHISTORY_DIR_IMAGE}/image-files/`dirname $f`
			cp ${IMAGE_ROOTFS}/$f ${BUILDHISTORY_DIR_IMAGE}/image-files/$f
		fi
	done

	# Record some machine-readable meta-information about the image
	printf ""  > ${BUILDHISTORY_DIR_IMAGE}/image-info.txt
	cat >> ${BUILDHISTORY_DIR_IMAGE}/image-info.txt <<END
${@buildhistory_get_imagevars(d)}
END
	imagesize=`du -ks ${IMAGE_ROOTFS} | awk '{ print $1 }'`
	echo "IMAGESIZE = $imagesize" >> ${BUILDHISTORY_DIR_IMAGE}/image-info.txt

	# Add some configuration information
	echo "${MACHINE}: ${IMAGE_BASENAME} configured for ${DISTRO} ${DISTRO_VERSION}" > ${BUILDHISTORY_DIR_IMAGE}/build-id.txt

	cat >> ${BUILDHISTORY_DIR_IMAGE}/build-id.txt <<END
${@buildhistory_get_build_id(d)}
END
}

def buildhistory_get_imagevars(d):
    if d.getVar('BB_WORKERCONTEXT') != '1':
        return ""
    imagevars = "DISTRO DISTRO_VERSION USER_CLASSES IMAGE_CLASSES IMAGE_FEATURES IMAGE_LINGUAS IMAGE_INSTALL BAD_RECOMMENDATIONS NO_RECOMMENDATIONS PACKAGE_EXCLUDE ROOTFS_POSTPROCESS_COMMAND IMAGE_POSTPROCESS_COMMAND"
    listvars = "USER_CLASSES IMAGE_CLASSES IMAGE_FEATURES IMAGE_LINGUAS IMAGE_INSTALL BAD_RECOMMENDATIONS PACKAGE_EXCLUDE"
    return outputvars(imagevars, listvars, d)

