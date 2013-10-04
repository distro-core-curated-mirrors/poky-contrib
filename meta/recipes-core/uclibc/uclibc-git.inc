<<<<<<< HEAD
SRCREV="f22cca4722fa66e424562e69f4afa2bca0af871d"

PV = "0.9.33+git${SRCPV}"

FILESPATH = "${@base_set_filespath([ '${FILE_DIRNAME}/uclibc-git' ], d)}"

SRC_URI = "git://uclibc.org/uClibc.git;branch=master \
	file://uClibc.machine \
	file://uClibc.distro \
	file://obstack.cfg \
	file://locale.cfg \
=======
SRCREV="cb43f2afba0633400387fa7c55dda3396517f58a"

DEFAULT_PREFERENCE = "-1"

PV = "0.9.33+git${SRCPV}"
PR = "${INC_PR}.4"

FILESPATH = "${@base_set_filespath([ '${FILE_DIRNAME}/uclibc-git' ], d)}"

SRC_URI = "git://uclibc.org/uClibc.git;branch=master;protocol=git \
	file://uClibc.machine \
	file://uClibc.distro \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
	file://uclibc_enable_log2_test.patch \
	file://powerpc_copysignl.patch \
	file://argp-support.patch \
	file://argp-headers.patch \
	file://remove_attribute_optimize_Os.patch \
	file://compile-arm-fork-with-O2.patch \
<<<<<<< HEAD
	file://orign_path.patch \
=======
	file://uclibc-execvpe.patch \
	file://orign_path.patch \
	file://dup3.patch \
	file://define-MSG_CMSG_CLOEXEC.patch \
	file://posix_fallocate.patch \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
	file://0001-atexit_old-Do-not-add-it-to-shared-libc.patch \
	file://0001-nptl-arm-Move-aeabi_read_tp-to-uclibc_nonshared.a.patch \
	file://0001-nptl-atfork-Hide-pthread_atfork-in-shared-versions.patch \
	file://0001-librt-Use-nodefaultlibs-instead-of-nostdlib.patch \
<<<<<<< HEAD
	file://0001-Revert-utent.c-wtent.c-move-functions-from-utxent.c.patch \
	file://0001-add-posix_fadvise-for-arm.patch \
=======
	file://mount.h-update.patch \
	file://0001-Revert-utent.c-wtent.c-move-functions-from-utxent.c.patch \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
	"
S = "${WORKDIR}/git"
