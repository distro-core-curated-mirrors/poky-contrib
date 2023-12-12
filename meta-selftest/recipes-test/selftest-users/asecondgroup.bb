SUMMARY = "asecondgroup"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

LICENSE = "MIT"

DEPENDS = "coreutils-native"


S = "${WORKDIR}"

inherit useradd allarch
USERADD_DEPENDS = "bfirstgroup"

USERADD_PACKAGES = "${PN}"

USERADD_PARAM:${PN} = "-r -g grouptest3 -G grouptest2 -s /sbin/nologin gt4"
GROUPADD_PARAM:${PN} = "-r grouptest3"

TESTDIR = "${D}${sysconfdir}/creategroup"

do_install() {
	install -d   ${TESTDIR}
	install -d   ${TESTDIR}/dir
	touch        ${TESTDIR}/file
	ln -s ./file ${TESTDIR}/symlink
	install -d   ${TESTDIR}/fifotest
	mkfifo       ${TESTDIR}/fifotest/fifo
}

FILES:${PN} = "${sysconfdir}/creategroup/*"

