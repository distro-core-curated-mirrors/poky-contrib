#
# Copyright (C) 2008 OpenedHand Ltd.
#

SUMMARY = "Profiling tools"
LICENSE = "MIT"

<<<<<<< HEAD
PR = "r3"
=======
PR = "r1"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

inherit packagegroup

PACKAGE_ARCH = "${MACHINE_ARCH}"

# For backwards compatibility after rename
RPROVIDES_${PN} = "task-core-tools-profile"
RREPLACES_${PN} = "task-core-tools-profile"
RCONFLICTS_${PN} = "task-core-tools-profile"

<<<<<<< HEAD
PROFILE_TOOLS_X = "${@base_contains('DISTRO_FEATURES', 'x11', 'sysprof', '', d)}"

=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
RRECOMMENDS_${PN} = "\
    perf \
    trace-cmd \
    kernel-module-oprofile \
    blktrace \
<<<<<<< HEAD
    ${PROFILE_TOOLS_X} \
=======
    sysprof \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    "

PROFILETOOLS = "\
    oprofile \
    oprofileui-server \
    powertop \
    latencytop \
<<<<<<< HEAD
    "
=======
    lttng-control \
    lttng-viewer"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

# systemtap needs elfutils which is not fully buildable on uclibc
# hence we exclude it from uclibc based builds
SYSTEMTAP = "systemtap"
SYSTEMTAP_libc-uclibc = ""
SYSTEMTAP_mips = ""
<<<<<<< HEAD
SYSTEMTAP_mips64 = ""
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
SYSTEMTAP_aarch64 = ""

# lttng-ust uses sched_getcpu() which is not there on uclibc
# for some of the architectures it can be patched to call the
# syscall directly but for x86_64 __NR_getcpu is a vsyscall
# which means we can not use syscall() to call it. So we ignore
# it for x86_64/uclibc

LTTNGUST = "lttng-ust"
LTTNGUST_libc-uclibc = ""
<<<<<<< HEAD
LTTNGUST_aarch64 = ""

LTTNGTOOLS = "lttng-tools"
LTTNGTOOLS_aarch64 = ""

LTTNGMODULES = "lttng-modules"
LTTNGMODULES_aarch64 = ""

BABELTRACE = "babeltrace"
BABELTRACE_aarch64 = ""

=======
LTTNGUST_mips = ""
LTTNGUST_aarch64 = ""

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
# valgrind does not work on mips

VALGRIND = "valgrind"
VALGRIND_libc-uclibc = ""
VALGRIND_mips = ""
<<<<<<< HEAD
VALGRIND_mips64 = ""
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
VALGRIND_arm = ""
VALGRIND_aarch64 = ""

#    exmap-console
#    exmap-server

<<<<<<< HEAD
RDEPENDS_${PN} = "\
    ${PROFILETOOLS} \
    ${LTTNGUST} \
    ${LTTNGTOOLS} \
    ${LTTNGMODULES} \
    ${BABELTRACE} \
=======
# At present we only build lttng-ust on
# qemux86/qemux86-64/qemuppc/qemuarm/emenlow/atom-pc since upstream liburcu
# (which is required by lttng-ust) may not build on other platforms, like
# MIPS.
RDEPENDS_${PN} = "\
    ${PROFILETOOLS} \
    ${LTTNGUST} \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    ${SYSTEMTAP} \
    ${VALGRIND} \
    "
