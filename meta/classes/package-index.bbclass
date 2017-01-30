python package_index_handler () {
    dd = d.createCopy()
    target_sysroot = dd.expand("${STAGING_DIR}/${MACHINE}")
    native_sysroot = dd.expand("${STAGING_DIR}/${BUILD_ARCH}")
    staging_populate_sysroot_dir(target_sysroot, native_sysroot, True, dd)

    dd.setVar("STAGING_DIR_NATIVE", native_sysroot)
    with oe.utils.environ(PATH=dd.getVar("PATH")):
        from oe.package_manager import generate_index_files
        generate_index_files(dd)
}

addhandler package_index_handler
package_index_handler[eventmask] = "bb.event.BuildCompleted"

do_build[depends] += "${PACKAGEINDEXDEPS}"
