DESCRIPTION = "A standalone image construction tool"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/LICENSE;md5=4d92cd373abda3937c2bc47fbc49d690 \
                    file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

INHIBIT_DEFAULT_DEPS = "1"

SRC_URI = "file://build-rootfs \
           file://run.sh \
           file://base.bbclass \
           file://README \
           file://bitbake.conf"

do_install () {
	cp -r ${COREBASE}/bitbake ${D}/
	rm ${D}/bitbake/toaster*
	rm -rf ${D}/bitbake/lib/toaster
	cp ${WORKDIR}/build-rootfs ${D}/bitbake/bin/
	cp ${WORKDIR}/run.sh ${D}
	mkdir -p ${D}/meta/classes
        for i in core-image image image_types image_types_uboot populate_sdk populate_sdk_base rootfs_ipk rootfs_deb rootfs_rpm utils; do
		cp ${COREBASE}/meta/classes/$i.bbclass ${D}/meta/classes
	done
	cp ${WORKDIR}/base.bbclass ${D}/meta/classes
	sed -i -e 's/runtime_mapping_rename/#runtime_mapping_rename/g' ${D}/meta/classes/image.bbclass
	sed -i -e 's/IMAGE_CLASSES +=/IMAGE_CLASSES ?=/' ${D}/meta/classes/image.bbclass
	for i in meta toolchain-scripts gzipnative siteinfo; do
		touch ${D}/meta/classes/$i.bbclass
	done
	mkdir -p ${D}/meta/lib/oe
	for i in __init__ data image maketype manifest packagegroup package_manager package path rootfs sdk types utils; do
		cp ${COREBASE}/meta/lib/oe/$i.py ${D}/meta/lib/oe
	done
	mkdir -p ${D}/meta/conf
	cp ${WORKDIR}/bitbake.conf ${D}/meta/conf
	cp ${WORKDIR}/README ${D}
	mkdir -p ${D}/meta/files
	cp ${COREBASE}/meta/files/toolchain-shar-template* ${D}/meta/files
	cp ${COREBASE}/meta/recipes-core/images/core-image-minimal.bb ${D}/meta
	
	mkdir -p ${D}/scripts/lib/wic
	cp ${COREBASE}/scripts/wic ${D}/scripts/
	cp -r ${COREBASE}/scripts/lib/wic/* ${D}/scripts/lib/wic/
	mkdir -p ${D}/scripts/lib/image
	cp -r ${COREBASE}/scripts/lib/image/* ${D}/scripts/lib/image
	
	
	cd ${D}
	tar -czf ${DEPLOY_DIR}/imagebuilder-collab.tgz .
}

deltask package
deltask package_write_rpm
deltask package_write_ipk
deltask package_write_deb

