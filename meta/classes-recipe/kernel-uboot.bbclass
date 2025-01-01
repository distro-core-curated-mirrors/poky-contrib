#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

# fitImage kernel compression algorithm
FIT_KERNEL_COMP_ALG ?= "gzip"
FIT_KERNEL_COMP_ALG_EXTENSION ?= ".gz"

# Kernel image type passed to mkimage (i.e. kernel kernel_noload...)
UBOOT_MKIMAGE_KERNEL_TYPE ?= "kernel"

def uboot_prep_kimage(d):
    import subprocess

    arch = d.getVar('ARCH')
    initramfs_image_bundle = d.getVar('INITRAMFS_IMAGE_BUNDLE')
    fit_kernel_comp_alg = d.getVar('FIT_KERNEL_COMP_ALG') or 'gzip'
    fit_kernel_comp_alg_extension = d.getVar('FIT_KERNEL_COMP_ALG_EXTENSION') or '.gz'
    kernel_objcopy = d.getVar('KERNEL_OBJCOPY')

    vmlinux_path = ""
    linux_suffix = ""
    linux_comp = "none"

    if os.path.exists(f'arch/{arch}/boot/compressed/vmlinux'):
        vmlinux_path = f'arch/{arch}/boot/compressed/vmlinux'
    elif os.path.exists(f'arch/{arch}/boot/vmlinuz.bin'):
        if os.path.exists('linux.bin'):
            os.remove('linux.bin')
        os.link(f'arch/{arch}/boot/vmlinuz.bin', 'linux.bin')
    else:
        vmlinux_path = 'vmlinux'
        # Use vmlinux.initramfs for linux.bin when INITRAMFS_IMAGE_BUNDLE set
        # As per the implementation in kernel.bbclass.
        # See do_bundle_initramfs function
        if initramfs_image_bundle == "1" and os.path.exists('vmlinux.initramfs'):
            vmlinux_path = 'vmlinux.initramfs'
        linux_suffix = fit_kernel_comp_alg_extension
        linux_comp = fit_kernel_comp_alg

    if vmlinux_path:
        subprocess.run([kernel_objcopy.strip(), '-O', 'binary', '-R', '.note', '-R', '.comment', '-S', os.path.abspath(vmlinux_path), 'linux.bin'], check=True)
        # if ret.returncode != 0:
        # bb.fatal(f"Error: stderr: {ret.stderr.decode('utf-8')}   stdout: {ret.stdout.decode('utf-8')}, vmlinux_path: {os.path.abspath(vmlinux_path)}, pwd: {os.getcwd()}, args: {ret.args}")

    if linux_comp != "none":
        if linux_comp == "gzip":
            subprocess.run(['gzip', '-9', 'linux.bin'], check=True)
        elif linux_comp == "lzo":
            subprocess.run(['lzop', '-9', 'linux.bin'], check=True)
        os.rename(f'linux.bin{linux_suffix}', 'linux.bin')

    return linux_comp
