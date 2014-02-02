SRC_URI = "git://tianocore.git.sourceforge.net/gitroot/tianocore/edk2 \
           file://edk2.git-09aaa4a8b51d30f13f55448f1368c5d55e7a6a67.patch \
           file://edk2.git-b06b0bf999a339ea094c932432fd8f8f86b4edd9.patch \
           file://edk2.git-dbe2d86515c07c5e0ac1c8e36db9e77fd3044781.patch \
           file://edk2.git-fb201bce9b42bb23ffe3bbc479424303f8133bf6.patch \
           file://edk2.git-70a3c7b64a263b57cec0ab7e93a60c8aa5397de0.gitpatch \
           "

S = "${WORKDIR}/git"

DEPENDS = "e2fsprogs acpica-native"

PV = "0.0+git${SRCPV}"
#SRCREV = "${AUTOREV}"
SRCREV = "b9b77ab1ba0e5138307150a1a3caa4342d464f16"

LICENSE = "intel"
LIC_FILES_CHKSUM = "file://BaseTools/License.txt;md5=a041d47c90fd51b4514d09a5127210e6 \
                    file://OvmfPkg/License.txt;md5=ffd52cf9a8e0e036b9a61a0de2dc87ed \
                   "

PARALLEL_MAKE = ""
ARCH = "X64"

do_gitpatch () {
	git apply ${WORKDIR}/edk2*.gitpatch
}
addtask gitpatch before do_configure after do_patch

do_configure () {
	sed -i -e 's/\(DEFINE.*UNIX_IASL_BIN.*=\).*$/\1 iasl/' ${S}/BaseTools/Conf/tools_def.template
}

do_compile () {
	cp ${STAGING_DATADIR}/seabios/Csm16.bin ${S}/OvmfPkg/Csm/Csm16/
	# Need to ensure this runs in a bash shell
	echo "#!/bin/bash
	.  ${S}/edksetup.sh
	cd ${S}/BaseTools/
	make ${PARALLEL_MAKE} ARCH='${ARCH}' CC='$CC' AS='$CC' ASL='iasl'
	cd ${S}/OvmfPkg/
	export ARCH='${ARCH}'
	./build.sh -D CSM_ENABLE
	" > ${WORKDIR}/real_compile
	chmod a+x ${WORKDIR}/real_compile
	bash ${WORKDIR}/real_compile
}

do_install () {
	install -d ${D}${datadir}/edk2/
	install ${S}/Build/OvmfX64/DEBUG_GCC48/FV/OVMF.fd ${D}${datadir}/edk2/
}