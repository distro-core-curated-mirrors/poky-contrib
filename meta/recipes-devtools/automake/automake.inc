SUMMARY = "A GNU tool for automatically generating Makefiles."
DESCRIPTION = "Automake is a tool for automatically generating `Makefile.in' files compliant with the GNU Coding \
Standards. Automake requires the use of Autoconf."
LICENSE = "GPLv2"
HOMEPAGE = "http://www.gnu.org/software/automake/"
SECTION = "devel"

SRC_URI = "${GNU_MIRROR}/automake/automake-${PV}.tar.gz"

inherit autotools

do_configure() {
	oe_runconf
}

<<<<<<< HEAD
export AUTOMAKE = "${@bb.utils.which('automake', d.getVar('PATH', True))}"
=======
export AUTOMAKE = "${@bb.which('automake', d.getVar('PATH', True))}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

FILES_${PN} += "${datadir}/automake* ${datadir}/aclocal*"
