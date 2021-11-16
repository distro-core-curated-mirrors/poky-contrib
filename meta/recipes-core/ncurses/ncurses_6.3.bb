require ncurses.inc

SRC_URI += "file://0001-tic-hang.patch \
           file://0002-configure-reproducible.patch \
           file://0003-gen-pkgconfig.in-Do-not-include-LDFLAGS-in-generated.patch \
           "
SRCREV = "deb0d07e8eb4803b9e9653359eab17a30d04369d"
S = "${WORKDIR}/git"
UPSTREAM_CHECK_GITTAGREGEX = "(?P<pver>\d+(\.\d+)+)$"

# This is needed when using patchlevel versions like 6.1+20181013
#CVE_VERSION = "${@d.getVar("PV").split('+')[0]}.${@d.getVar("PV").split('+')[1]}"
