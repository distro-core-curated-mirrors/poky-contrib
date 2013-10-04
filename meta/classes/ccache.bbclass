<<<<<<< HEAD
CCACHE = "${@bb.utils.which(d.getVar('PATH', True), 'ccache') and 'ccache '}"
export CCACHE_DIR ?= "${TMPDIR}/ccache/${MULTIMACH_HOST_SYS}/${PN}"
=======
CCACHE = "${@bb.which(d.getVar('PATH', True), 'ccache') and 'ccache '}"
export CCACHE_DIR = "${TMPDIR}/ccache/${MULTIMACH_HOST_SYS}/${PN}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
CCACHE_DISABLE[unexport] = "1"

do_configure[dirs] =+ "${CCACHE_DIR}"
do_kernel_configme[dirs] =+ "${CCACHE_DIR}"

do_clean[cleandirs] += "${CCACHE_DIR}"
