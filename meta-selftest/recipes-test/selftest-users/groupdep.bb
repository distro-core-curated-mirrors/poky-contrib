SUMMARY = "groupdep"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

LICENSE = "MIT"

DEPENDS = "coreutils-native cthirdgroup"

S = "${WORKDIR}"

TESTDIR = "${D}${sysconfdir}/creategroup"

do_install() {
	install -d   ${TESTDIR}
	install -d   ${TESTDIR}/dir
	touch        ${TESTDIR}/file
	ln -s ./file ${TESTDIR}/symlink
	install -d   ${TESTDIR}/fifotest
	mkfifo       ${TESTDIR}/fifotest/fifo
	chown  gt3:grouptest2 ${TESTDIR}/file
	chown -R gt3:grouptest2 ${TESTDIR}/dir
	chown -h gt4:grouptest3 ${TESTDIR}/symlink
	chown -R gt4:grouptest3 ${TESTDIR}/fifotest
}

FILES:${PN} = "${sysconfdir}/creategroup/*"
