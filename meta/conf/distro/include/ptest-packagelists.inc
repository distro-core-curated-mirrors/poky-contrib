#
# Lists of the ptests in OE-Core, sorted into two sets by the time they take
#
# ptests which take less than ~30s each
#
PTESTS_FAST = "\
    python3-cryptography \
"
PTESTS_FAST:append:libc-glibc = " glibc-y2038-tests"
PTESTS_PROBLEMS:remove:libc-glibc = "glibc-y2038-tests"
PTESTS_FAST:remove:mips64 = "qemu"
PTESTS_PROBLEMS:append:mips64 = " qemu"
PTESTS_FAST:remove:riscv32 = "qemu"
PTESTS_PROBLEMS:append:riscv32 = " qemu"

PTESTS_SLOW = "\
"

# python3 ptests hang on qemuriscv64
PTESTS_SLOW:remove:riscv64 = "valgrind python3"
PTESTS_PROBLEMS:append:riscv64 = " valgrind python3"
PTESTS_SLOW:remove:riscv32 = "lttng-tools strace valgrind"
PTESTS_PROBLEMS:append:riscv32 = " lttng-tools strace valgrind"
PTESTS_SLOW:append:libc-musl = " libc-test"
PTESTS_SLOW:remove:x86 = "valgrind"
PTESTS_PROBLEMS:append:x86 = " valgrind"

#    ruby \ # Timeout
#    rt-tests \ # Needs to be checked whether it runs at all
#    bash \ # Test outcomes are non-deterministic by design
#    ifupdown \ # Tested separately in lib/oeqa/selftest/cases/imagefeatures.py
#    libinput \ # Tests need an unloaded system to be reliable
#    libpam \ # Needs pam DISTRO_FEATURE
#    mdadm \ # tests are flaky in AB.
#    numactl \ # qemu not (yet) configured for numa; all tests are skipped
#    libseccomp \ #  tests failed: 38; add to slow tests once addressed
#    python3-numpy \ # requires even more RAM and (possibly) disk space; multiple failures

PTESTS_PROBLEMS = "\
    ruby \
    rt-tests \
    bash \
    ifupdown \
    libinput \
    libpam \
    libseccomp \
    mdadm \
    numactl \
    python3-license-expression \
    python3-numpy \
"
