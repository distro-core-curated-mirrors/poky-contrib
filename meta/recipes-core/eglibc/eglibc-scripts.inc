include eglibc-collateral.inc

SUMMARY = "utility scripts provided by eglibc"
DESCRIPTION = "utility scripts provided by eglibc"
<<<<<<< HEAD
RDEPENDS_${PN} = "bash eglibc-mtrace"

SRC = "${STAGING_INCDIR}/eglibc-scripts-internal-${MULTIMACH_TARGET_SYS}"

bashscripts = "sotruss xtrace"
=======
RDEPENDS_${PN} = "bash"
RDEPENDS_ldd = "bash"

SRC = "${STAGING_INCDIR}/eglibc-scripts-internal-${MULTIMACH_TARGET_SYS}"

bashscripts = "mtrace sotruss xtrace"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

do_install() {
	install -d -m 0755 ${D}${bindir}
	for i in ${bashscripts}; do
		install -m 0755 ${SRC}/$i ${D}${bindir}/
	done
}
