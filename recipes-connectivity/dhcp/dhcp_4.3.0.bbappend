inherit with-selinux

FILESEXTRAPATHS_prepend := "${@target_selinux(d, '${THISDIR}/files:')}"
