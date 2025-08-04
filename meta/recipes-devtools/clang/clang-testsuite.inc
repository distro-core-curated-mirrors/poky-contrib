# clang-testsuite.inc
# Native-only test setup for Clang using lit (LLVM Integrated Tester)

SUMMARY = "Clang TestSuite"

inherit qemu

TARGETS ?= "clang llvm lld"

python check_prepare() {
    import os

    builddir = d.getVar("BUILDDIR")
    lit_site_cfg = os.path.join(builddir, "ex.lit.site.cfg")
    bb.note("Generating LIT site config at: %s" % lit_site_cfg)

    with open(lit_site_cfg, "w") as f:
        f.write("# Auto-generated LIT site config for native testing\n")
        f.write("config.target_triple = '{}'\n".format(d.getVar('TARGET_SYS')))
        f.write("config.host_cxx = '{}clang++'\n".format(d.getVar('STAGING_BINDIR_NATIVE') + "/"))
        f.write("config.host_cc = '{}clang'\n".format(d.getVar('STAGING_BINDIR_NATIVE') + "/"))
        f.write("config.llvm_tools_dir = '{}'\n".format(d.getVar('STAGING_BINDIR_NATIVE')))
        f.write("config.cc = config.host_cc\n")
        f.write("config.cxx = config.host_cxx\n")
        f.write("config.use_lit_shell = True\n")
        f.write("config.target_arch = '{}'\n".format(d.getVar('TARGET_ARCH')))
        f.write("config.test_source_root = '{}'\n".format(workdir))  # Optional
        f.write("config.test_exec_root = '{}'\n".format(workdir))    # Optional

    # Dump key environment variables to a file for debugging
    env_debug_file = os.path.join(builddir, "env-vars-debug.txt")
    with open(env_debug_file, "w") as f:
        f.write("### Yocto Environment Variables at check_prepare ###\n")
        for key in sorted(d.keys()):
            f.write(f"{key} = {d.getVar(key)}\n")

    bb.note("Environment variable dump written to: %s" % env_debug_file)
}

do_check() {
    bbnote "=== BEGIN: Clang LIT Testing ==="
    bbnote "Working directory: ${WORKDIR}"
    bbnote "BUILD DIR (B)    : ${B}"
    bbnote "SOURCE DIR (S)   : ${S}"
    bbnote "Target Triple    : ${TARGET_SYS}"
    bbnote "Host Clang       : ${STAGING_BINDIR_NATIVE}/clang"
    bbnote "Host Clang++     : ${STAGING_BINDIR_NATIVE}/clang++"
    bbnote "CHECK_TARGET     : ${CHECK_TARGET}"
    bbnote "LIT Arguments    : ${LIT_ARGS}"
    bbnote "PATH             : $PATH"

    # Optionally show contents of LIT config
    bbnote "Contents of lit.site.cfg:"
    cat ${WORKDIR}/lit.site.cfg || bbwarn "lit.site.cfg missing!"

    # Show environment snapshot (already written by check_prepare)
    bbnote "Environment snapshot written to: ${WORKDIR}/env-vars-debug.txt"

    cd ${B}
    bbnote "Running tests::"
    # ninja check-clang
    for target in ${TARGETS}; do
        bbnote "Running test target: ninja check-${target}"
        if ! ${B}/bin/llvm-lit -v ${S}/${target}/test -o check-${target}-result.json ; then 
            bbwarn "Clang test target 'check-${target}' failed. Check logs."
            exit 1
        fi
    done

    bbnote "All test targets in CHECK_TARGET completed successfully."
    bbnote "=== END: Clang LIT Testing ==="
}

addtask check after do_compile do_install
do_check[depends] += "ninja-native:do_populate_sysroot clang-native:do_populate_sysroot"

