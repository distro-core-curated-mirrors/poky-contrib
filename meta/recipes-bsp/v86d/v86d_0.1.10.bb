DESCRIPTION = "User support binary for the uvesafb kernel module"
HOMEPAGE = "http://dev.gentoo.org/~spock/projects/uvesafb/"

# the copyright info is at the bottom of README, expect break
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://README;md5=94ac1971e4f2309dc322d598e7b1f7dd"

DEPENDS = "virtual/kernel"
RRECOMMENDS_${PN} = "kernel-module-uvesafb"
PR = "r1"

<<<<<<< HEAD
SRC_URI = "http://distfiles.gentoo.org/distfiles/${BP}.tar.bz2 \
=======
SRC_URI = "http://dev.gentoo.org/~spock/projects/uvesafb/archive/v86d-${PV}.tar.bz2 \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
           file://fbsetup \
           file://ar-from-env.patch"

SRC_URI[md5sum] = "51c792ba7b874ad8c43f0d3da4cfabe0"
SRC_URI[sha256sum] = "634964ae18ef68c8493add2ce150e3b4502badeb0d9194b4bd81241d25e6735c"

PACKAGE_ARCH = "${MACHINE_ARCH}"
<<<<<<< HEAD
COMPATIBLE_HOST = '(i.86|x86_64).*-linux'
=======
COMPATIBLE_MACHINE = "(qemux86)"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

INITSCRIPT_NAME = "fbsetup"
INITSCRIPT_PARAMS = "start 0 S ."

do_configure () {
	./configure --with-x86emu
}

do_compile () {
<<<<<<< HEAD
	KDIR="${STAGING_DIR_HOST}/usr" make
=======
	KDIR="${STAGING_KERNEL_DIR}" make
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
}

do_install () {
	install -d ${D}${base_sbindir}
	install v86d ${D}${base_sbindir}/

        install -d ${D}${sysconfdir}/init.d/
        install -m 0755 ${WORKDIR}/fbsetup ${D}${sysconfdir}/init.d/fbsetup
}

inherit update-rc.d
