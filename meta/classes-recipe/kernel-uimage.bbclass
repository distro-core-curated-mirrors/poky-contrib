#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

inherit kernel-uboot

python __anonymous () {
    if "uImage" in d.getVar('KERNEL_IMAGETYPES'):
        depends = d.getVar("DEPENDS")
        depends = "%s u-boot-tools-native" % depends
        d.setVar("DEPENDS", depends)

        # Override KERNEL_IMAGETYPE_FOR_MAKE variable, which is internal
        # to kernel.bbclass . We override the variable here, since we need
        # to build uImage using the kernel build system if and only if
        # KEEPUIMAGE == yes. Otherwise, we pack compressed vmlinux into
        # the uImage .
        if d.getVar("KEEPUIMAGE") != 'yes':
            typeformake = d.getVar("KERNEL_IMAGETYPE_FOR_MAKE") or ""
            if "uImage" in typeformake.split():
                d.setVar('KERNEL_IMAGETYPE_FOR_MAKE', typeformake.replace('uImage', 'vmlinux'))

            # Enable building of uImage with mkimage
            bb.build.addtask('do_uboot_mkimage', 'do_install', 'do_kernel_link_images', d)
}

do_uboot_mkimage[dirs] += "${B}"
python do_uboot_mkimage() {
    import subprocess

    uboot_prep_kimage()

    entrypoint = d.getVar('UBOOT_ENTRYPOINT')
    if d.getVar('UBOOT_ENTRYSYMBOL'):
        entrysymbol = d.getVar('UBOOT_ENTRYSYMBOL')
        vmlinux_path = os.path.join(d.getVar('B'), 'vmlinux')
        entrypoint = subprocess.check_output(
            f"{d.getVar('HOST_PREFIX')}nm {vmlinux_path} | awk '$3==\"{entrysymbol}\" {{print \"0x\"$1;exit}}'",
            shell=True
        ).strip().decode('utf-8')

    uboot_mkimage_cmd = (
        f"uboot-mkimage -A {d.getVar('UBOOT_ARCH')} -O linux -T {d.getVar('UBOOT_MKIMAGE_KERNEL_TYPE')} "
        f"-C {d.getVar('linux_comp')} -a {d.getVar('UBOOT_LOADADDRESS')} -e {entrypoint} "
        f"-n \"{d.getVar('DISTRO_NAME')}/{d.getVar('PV')}/{d.getVar('MACHINE')}\" "
        f"-d linux.bin {os.path.join(d.getVar('B'), 'arch', d.getVar('ARCH'), 'boot', 'uImage')}"
    )
    subprocess.run(uboot_mkimage_cmd, shell=True, check=True)
    if os.path.exists('linux.bin'):
        os.remove('linux.bin')
}
