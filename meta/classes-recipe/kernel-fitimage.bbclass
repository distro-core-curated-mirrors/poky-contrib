#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

inherit kernel-uboot kernel-artifact-names uboot-config

def get_fit_replacement_type(d):
    kerneltypes = d.getVar('KERNEL_IMAGETYPES') or ""
    replacementtype = ""
    if 'fitImage' in kerneltypes.split():
        uarch = d.getVar("UBOOT_ARCH")
        if uarch == "arm64":
            replacementtype = "Image"
        elif uarch == "riscv":
            replacementtype = "Image"
        elif uarch == "mips":
            replacementtype = "vmlinuz.bin"
        elif uarch == "x86":
            replacementtype = "bzImage"
        elif uarch == "microblaze":
            replacementtype = "linux.bin"
        else:
            replacementtype = "zImage"
    return replacementtype

KERNEL_IMAGETYPE_REPLACEMENT ?= "${@get_fit_replacement_type(d)}"
DEPENDS:append = " ${@'u-boot-tools-native dtc-native' if 'fitImage' in (d.getVar('KERNEL_IMAGETYPES') or '').split() else ''}"

python __anonymous () {
        # Override KERNEL_IMAGETYPE_FOR_MAKE variable, which is internal
        # to kernel.bbclass . We have to override it, since we pack zImage
        # (at least for now) into the fitImage .
        typeformake = d.getVar("KERNEL_IMAGETYPE_FOR_MAKE") or ""
        if 'fitImage' in typeformake.split():
            d.setVar('KERNEL_IMAGETYPE_FOR_MAKE', typeformake.replace('fitImage', d.getVar('KERNEL_IMAGETYPE_REPLACEMENT')))

        image = d.getVar('INITRAMFS_IMAGE')
        if image:
            d.appendVarFlag('do_assemble_fitimage_initramfs', 'depends', ' ${INITRAMFS_IMAGE}:do_image_complete')

        ubootenv = d.getVar('UBOOT_ENV')
        if ubootenv:
            d.appendVarFlag('do_assemble_fitimage', 'depends', ' virtual/bootloader:do_populate_sysroot')

        #check if there are any dtb providers
        providerdtb = d.getVar("PREFERRED_PROVIDER_virtual/dtb")
        if providerdtb:
            d.appendVarFlag('do_assemble_fitimage', 'depends', ' virtual/dtb:do_populate_sysroot')
            d.appendVarFlag('do_assemble_fitimage_initramfs', 'depends', ' virtual/dtb:do_populate_sysroot')
            d.setVar('EXTERNAL_KERNEL_DEVICETREE', "${RECIPE_SYSROOT}/boot/devicetree")
}


# Description string
FIT_DESC ?= "Kernel fitImage for ${DISTRO_NAME}/${PV}/${MACHINE}"

# Kernel fitImage Hash Algo
FIT_HASH_ALG ?= "sha256"

# Kernel fitImage Signature Algo
FIT_SIGN_ALG ?= "rsa2048"

# Kernel / U-Boot fitImage Padding Algo
FIT_PAD_ALG ?= "pkcs-1.5"

# Generate keys for signing Kernel fitImage
FIT_GENERATE_KEYS ?= "0"

# Size of private keys in number of bits
FIT_SIGN_NUMBITS ?= "2048"

# args to openssl genrsa (Default is just the public exponent)
FIT_KEY_GENRSA_ARGS ?= "-F4"

# args to openssl req (Default is -batch for non interactive mode and
# -new for new certificate)
FIT_KEY_REQ_ARGS ?= "-batch -new"

# Standard format for public key certificate
FIT_KEY_SIGN_PKCS ?= "-x509"

# Sign individual images as well
FIT_SIGN_INDIVIDUAL ?= "0"

FIT_CONF_PREFIX ?= "conf-"
FIT_CONF_PREFIX[doc] = "Prefix to use for FIT configuration node name"

FIT_SUPPORTED_INITRAMFS_FSTYPES ?= "cpio.lz4 cpio.lzo cpio.lzma cpio.xz cpio.zst cpio.gz ext2.gz cpio"

# Allow user to select the default DTB for FIT image when multiple dtb's exists.
FIT_CONF_DEFAULT_DTB ?= ""

# length of address in number of <u32> cells
# ex: 1 32bits address, 2 64bits address
FIT_ADDRESS_CELLS ?= "1"

# Keys used to sign individually image nodes.
# The keys to sign image nodes must be different from those used to sign
# configuration nodes, otherwise the "required" property, from
# UBOOT_DTB_BINARY, will be set to "conf", because "conf" prevails on "image".
# Then the images signature checking will not be mandatory and no error will be
# raised in case of failure.
# UBOOT_SIGN_IMG_KEYNAME = "dev2" # keys name in keydir (eg. "dev2.crt", "dev2.key")

#
# Emit the fitImage ITS header
#
def fitimage_emit_fit_header(d, itsfile):
    with open(itsfile, 'a') as f:
        f.write("/dts-v1/;\n\n/ {\n")
        f.write(f'        description = "{d.getVar('FIT_DESC')}";\n')
        f.write(f'        #address-cells = <{d.getVar('FIT_ADDRESS_CELLS')}>;\n')

#
# Emit the fitImage section bits
#
# section_type: imagestart - image section start
#               confstart  - configuration section start
#               sectend    - section end
#               fitend     - fitimage end
def fitimage_emit_section_maint(itsfile, section_type):
    with open(itsfile, 'a') as f:
        if section_type == "imagestart":
            f.write("\n        images {\n")
        elif section_type == "confstart":
            f.write("\n        configurations {\n")
        elif section_type == "sectend":
            f.write("};\n")
        elif section_type == "fitend":
            f.write("};\n")

#
# Emit the fitImage ITS kernel section
#
def fitimage_emit_section_kernel(d, itsfile, kernel_id, kernel_path, compression):
    import subprocess

    kernel_csum = d.getVar("FIT_HASH_ALG")
    kernel_sign_algo = d.getVar("FIT_SIGN_ALG")
    kernel_sign_keyname = d.getVar("UBOOT_SIGN_IMG_KEYNAME")

    entrypoint = d.getVar("UBOOT_ENTRYPOINT")
    if d.getVar("UBOOT_ENTRYSYMBOL"):
        entrypoint = subprocess.check_output(
            f"{d.getVar('HOST_PREFIX')}nm vmlinux | awk '$3==\"{d.getVar('UBOOT_ENTRYSYMBOL')}\" {{print \"0x\"$1;exit}}'",
            shell=True
        ).strip().decode()

    with open(itsfile, 'a') as f:
        f.write(f"""
                kernel-{kernel_id} {{
                        description = "Linux kernel";
                        data = /incbin/("{kernel_path}");
                        type = "{d.getVar('UBOOT_MKIMAGE_KERNEL_TYPE')}";
                        arch = "{d.getVar('UBOOT_ARCH')}";
                        os = "linux";
                        compression = "{compression}";
                        load = <{d.getVar('UBOOT_LOADADDRESS')}>;
                        entry = <{entrypoint}>;
                        hash-1 {{
                                algo = "{kernel_csum}";
                        }};
        """)

        if d.getVar("UBOOT_SIGN_ENABLE") == "1" and d.getVar("FIT_SIGN_INDIVIDUAL") == "1" and kernel_sign_keyname:
            f.write(f"""
                        signature-1 {{
                                algo = "{kernel_csum},{kernel_sign_algo}";
                                key-name-hint = "{kernel_sign_keyname}";
                        }};
            """)

        f.write("""
                };
        """)

#
# Emit the fitImage ITS DTB section
#
def fitimage_emit_section_dtb(d, itsfile, dtb_id, dtb_path):
    dtb_csum = d.getVar("FIT_HASH_ALG")
    dtb_sign_algo = d.getVar("FIT_SIGN_ALG")
    dtb_sign_keyname = d.getVar("UBOOT_SIGN_IMG_KEYNAME")

    dtb_loadline = ""
    dtb_ext = os.path.splitext(dtb_path)[1]
    if dtb_ext == ".dtbo":
        if d.getVar("UBOOT_DTBO_LOADADDRESS"):
            dtb_loadline = f"load = <{d.getVar('UBOOT_DTBO_LOADADDRESS')}>;"
    elif d.getVar("UBOOT_DTB_LOADADDRESS"):
        dtb_loadline = f"load = <{d.getVar('UBOOT_DTB_LOADADDRESS')}>;"

    with open(itsfile, 'a') as f:
        f.write(f"""
                fdt-{dtb_id} {{
                        description = "Flattened Device Tree blob";
                        data = /incbin/("{dtb_path}");
                        type = "flat_dt";
                        arch = "{d.getVar('UBOOT_ARCH')}";
                        compression = "none";
                        {dtb_loadline}
                        hash-1 {{
                                algo = "{dtb_csum}";
                        }};
        """)

        if d.getVar("UBOOT_SIGN_ENABLE") == "1" and d.getVar("FIT_SIGN_INDIVIDUAL") == "1" and dtb_sign_keyname:
            f.write(f"""
                        signature-1 {{
                                algo = "{dtb_csum},{dtb_sign_algo}";
                                key-name-hint = "{dtb_sign_keyname}";
                        }};
            """)

        f.write("""
                };
        """)

#
# Emit the fitImage ITS u-boot script section
#
def fitimage_emit_section_boot_script(d, itsfile, bootscr_id, bootscr_path):
    bootscr_csum = d.getVar("FIT_HASH_ALG")
    bootscr_sign_algo = d.getVar("FIT_SIGN_ALG")
    bootscr_sign_keyname = d.getVar("UBOOT_SIGN_IMG_KEYNAME")

    with open(itsfile, 'a') as f:
        f.write(f"""
                bootscr-{bootscr_id} {{
                        description = "U-boot script";
                        data = /incbin/("{bootscr_path}");
                        type = "script";
                        arch = "{d.getVar('UBOOT_ARCH')}";
                        compression = "none";
                        hash-1 {{
                                algo = "{bootscr_csum}";
                        }};
        """)

        if d.getVar("UBOOT_SIGN_ENABLE") == "1" and d.getVar("FIT_SIGN_INDIVIDUAL") == "1" and bootscr_sign_keyname:
            f.write(f"""
                        signature-1 {{
                                algo = "{bootscr_csum},{bootscr_sign_algo}";
                                key-name-hint = "{bootscr_sign_keyname}";
                        }};
            """)

        f.write("""
                };
        """)

#
# Emit the fitImage ITS setup section
#
def fitimage_emit_section_setup(d, itsfile, setup_id, setup_path):
    setup_csum = d.getVar("FIT_HASH_ALG")

    with open(itsfile, 'a') as f:
        f.write(f"""
                setup-{setup_id} {{
                        description = "Linux setup.bin";
                        data = /incbin/("{setup_path}");
                        type = "x86_setup";
                        arch = "{d.getVar('UBOOT_ARCH')}";
                        os = "linux";
                        compression = "none";
                        load = <0x00090000>;
                        entry = <0x00090000>;
                        hash-1 {{
                                algo = "{setup_csum}";
                        }};
                }};
        """)

#
# Emit the fitImage ITS ramdisk section
#
def fitimage_emit_section_ramdisk(d, itsfile, ramdisk_id, ramdisk_path):
    ramdisk_csum = d.getVar("FIT_HASH_ALG")
    ramdisk_sign_algo = d.getVar("FIT_SIGN_ALG")
    ramdisk_sign_keyname = d.getVar("UBOOT_SIGN_IMG_KEYNAME")
    ramdisk_loadline = ""
    ramdisk_entryline = ""

    if d.getVar("UBOOT_RD_LOADADDRESS"):
        ramdisk_loadline = f"load = <{d.getVar('UBOOT_RD_LOADADDRESS')}>;"
    if d.getVar("UBOOT_RD_ENTRYPOINT"):
        ramdisk_entryline = f"entry = <{d.getVar('UBOOT_RD_ENTRYPOINT')}>;"

    with open(itsfile, 'a') as f:
        f.write(f"""
                ramdisk-{ramdisk_id} {{
                        description = "{d.getVar('INITRAMFS_IMAGE')}";
                        data = /incbin/("{ramdisk_path}");
                        type = "ramdisk";
                        arch = "{d.getVar('UBOOT_ARCH')}";
                        os = "linux";
                        compression = "none";
                        {ramdisk_loadline}
                        {ramdisk_entryline}
                        hash-1 {{
                                algo = "{ramdisk_csum}";
                        }};
        """)

        if d.getVar("UBOOT_SIGN_ENABLE") == "1" and d.getVar("FIT_SIGN_INDIVIDUAL") == "1" and ramdisk_sign_keyname:
            f.write(f"""
                        signature-1 {{
                                algo = "{ramdisk_csum},{ramdisk_sign_algo}";
                                key-name-hint = "{ramdisk_sign_keyname}";
                        }};
            """)

        f.write("""
                };
        """)

#
# returns symlink destination if it points below directory
#
def symlink_points_below(file_or_symlink, expected_parent_dir):
    file_path = os.path.join(expected_parent_dir, file_or_symlink)
    if not os.path.islink(file_path):
        return None

    realpath = os.path.relpath(os.path.realpath(file_path), expected_parent_dir)
    if realpath.startswith(".."):
        return None

    return realpath

#
# Emit the fitImage ITS configuration section
#
def fitimage_emit_section_config(d, itsfile, kernel_id, dtb_image, ramdisk_id, bootscr_id, config_id, default_flag, default_dtb_image):
    import subprocess

    conf_csum = d.getVar("FIT_HASH_ALG")
    conf_sign_algo = d.getVar("FIT_SIGN_ALG")
    conf_padding_algo = d.getVar("FIT_PAD_ALG")
    conf_sign_keyname = d.getVar("UBOOT_SIGN_KEYNAME") if d.getVar("UBOOT_SIGN_ENABLE") == "1" else None

    conf_desc = []
    conf_node = d.getVar("FIT_CONF_PREFIX")
    kernel_line = ""
    fdt_line = ""
    ramdisk_line = ""
    bootscr_line = ""
    setup_line = ""
    default_line = ""
    compatible_line = ""

    dtb_image_sect = dtb_image
    if d.getVar("EXTERNAL_KERNEL_DEVICETREE"):
        dtb_image_sect = symlink_points_below(dtb_image, d.getVar("EXTERNAL_KERNEL_DEVICETREE"))

    dtb_path = d.getVar("EXTERNAL_KERNEL_DEVICETREE") or "" + '/' + dtb_image_sect
    if os.path.exists(dtb_path):
        try:
            ret = subprocess.run(["fdtget", "-t", "s", dtb_path, "/", "compatible"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            compat = ret.stdout.decode().strip().replace(" ", '", "')
            opt_props["compatible"] = f"{compat}"
        except subprocess.CalledProcessError as e:
            bb.debug(f"Failed to get 'compatible' property from {dtb_path}: stdout: {e.output.decode().strip()}, stderr: {e.stderr.decode().strip()}")

    dtb_image = dtb_image.replace('/', '_')
    dtb_image_sect = dtb_image_sect.replace('/', '_')

    # conf node name is selected based on dtb ID if it is present,
    # otherwise its selected based on kernel ID
    if dtb_image:
        conf_node += dtb_image
    else:
        conf_node += str(kernel_id)

    if kernel_id:
        conf_desc.append("Linux kernel")
        kernel_line = f'kernel = "kernel-{kernel_id}";'

    if dtb_image:
        conf_desc.append("FDT blob")
        fdt_line = f'fdt = "fdt-{dtb_image_sect}";'

    if ramdisk_id:
        conf_desc.append("ramdisk")
        ramdisk_line = f'ramdisk = "ramdisk-{ramdisk_id}";'

    if bootscr_id:
        conf_desc.append("u-boot script")
        bootscr_line = f'bootscr = "bootscr-{bootscr_id}";'

    if config_id:
        conf_desc.append("setup")
        setup_line = f'setup = "setup-{config_id}";'

    if default_flag == 1:
        if dtb_image:
            default_line = f'default = "{d.getVar("FIT_CONF_PREFIX")}{default_dtb_image or dtb_image}";'
        else:
            default_line = f'default = "{d.getVar("FIT_CONF_PREFIX")}{kernel_id}";'

    with open(itsfile, 'a') as f:
        f.write(f"""
                {default_line}
                {conf_node} {{
                        description = "{default_flag} {', '.join(conf_desc)}";
                        {compatible_line}
                        {kernel_line}
                        {fdt_line}
                        {ramdisk_line}
                        {bootscr_line}
                        {setup_line}
                        hash-1 {{
                                algo = "{conf_csum}";
                        }};
        """)

        if conf_sign_keyname:
            sign_entries = []
            if kernel_id:
                sign_entries.append("kernel")
            if dtb_image:
                sign_entries.append("fdt")
            if ramdisk_id:
                sign_entries.append("ramdisk")
            if bootscr_id:
                sign_entries.append("bootscr")
            if config_id:
                sign_entries.append("setup")
            sign_line = 'sign-images = ' + ', '.join('"%s"' % entry for entry in sign_entries) + ';'
            f.write(f"""
                        signature-1 {{
                                algo = "{conf_csum},{conf_sign_algo}";
                                key-name-hint = "{conf_sign_keyname}";
                                padding = "{conf_padding_algo}";
                                {sign_line}
                        }};
            """)

        f.write("""
                };
        """)

def fitimage_assemble(d, itsfile, fitname, ramdiskcount):
    import glob
    import shutil
    import subprocess

    kernelcount=1
    dtbcount=""
    DTBS=""
    setupcount=""
    bootscr_id=""
    default_dtb_image=""

    for f in [itsfile, os.path.join("arch", d.getVar("ARCH"), "boot", fitname)]:
        if os.path.exists(f):
            os.remove(f)

    if d.getVar("UBOOT_SIGN_IMG_KEYNAME") and d.getVar("UBOOT_SIGN_KEYNAME") == d.getVar("UBOOT_SIGN_IMG_KEYNAME"):
        bb.fatal("Keys used to sign images and configuration nodes must be different.")

    fitimage_emit_fit_header(d, itsfile)

    #
    # Step 1: Prepare a kernel image section.
    #
    fitimage_emit_section_maint(itsfile, "imagestart")

    linux_comp = uboot_prep_kimage(d)
    fitimage_emit_section_kernel(d, itsfile, kernelcount, "linux.bin", linux_comp)

    #
    # Step 2: Prepare a DTB image section
    #
    if d.getVar("KERNEL_DEVICETREE"):
        dtbcount = 1
        for DTB in d.getVar("KERNEL_DEVICETREE").split():
            if "/dts/" in DTB:
                bb.warn(f"{DTB} contains the full path to the dts file, but only the dtb name should be used.")
                DTB = os.path.basename(DTB).replace(".dts", ".dtb")

            # Skip DTB if it's also provided in EXTERNAL_KERNEL_DEVICETREE
            if d.getVar("EXTERNAL_KERNEL_DEVICETREE"):
                ext_dtb_path = os.path.join(d.getVar("EXTERNAL_KERNEL_DEVICETREE"), DTB)
                if os.path.exists(ext_dtb_path) and os.path.getsize(ext_dtb_path) > 0:
                    continue

            DTB_PATH = os.path.join(d.getVar("KERNEL_OUTPUT_DIR"), "dts", DTB)
            if not os.path.exists(DTB_PATH):
                DTB_PATH = os.path.join(d.getVar("KERNEL_OUTPUT_DIR"), DTB)

            # Strip off the path component from the filename
            if not oe.types.boolean(d.getVar("KERNEL_DTBVENDORED")):
                DTB = os.path.basename(DTB)

            # Set the default dtb image if it exists in the devicetree.
            if d.getVar("FIT_CONF_DEFAULT_DTB") == DTB:
                default_dtb_image = DTB.replace("/", "_")

            DTB = DTB.replace("/", "_")

            # Skip DTB if we've picked it up previously
            if DTB in DTBS.split():
                continue

            DTBS += " " + DTB
            fitimage_emit_section_dtb(d, itsfile, DTB, DTB_PATH)

    if d.getVar("EXTERNAL_KERNEL_DEVICETREE"):
        dtbcount = 1
        dtb_files = []
        for ext in ['*.dtb', '*.dtbo']:
            dtb_files.extend(sorted(glob.glob(os.path.join(d.getVar("EXTERNAL_KERNEL_DEVICETREE"), ext))))
        
        for dtb_path in dtb_files:
            dtb_name = os.path.relpath(dtb_path, d.getVar("EXTERNAL_KERNEL_DEVICETREE"))
            dtb_name_underscore = dtb_name.replace('/', '_')

            # Set the default dtb image if it exists in the devicetree.
            if d.getVar("FIT_CONF_DEFAULT_DTB") == dtb_name:
                default_dtb_image = dtb_name_underscore

            # Skip DTB/DTBO if we've picked it up previously
            if dtb_name_underscore in DTBS.split():
                continue

            DTBS += " " + dtb_name_underscore

            # Also skip if a symlink. We'll later have each config section point at it
            if symlink_points_below(dtb_name, d.getVar("EXTERNAL_KERNEL_DEVICETREE")):
                continue

            fitimage_emit_section_dtb(d, itsfile, dtb_name_underscore, dtb_path)

    if d.getVar("FIT_CONF_DEFAULT_DTB") and not default_dtb_image:
        bb.warn("%s is not available in the list of device trees." % d.getVar('FIT_CONF_DEFAULT_DTB'))

    #
    # Step 3: Prepare a u-boot script section
    #
    uboot_env = d.getVar("UBOOT_ENV")
    staging_dir_host = d.getVar("STAGING_DIR_HOST")
    uboot_env_binary = d.getVar("UBOOT_ENV_BINARY")

    if uboot_env and os.path.isdir(os.path.join(staging_dir_host, "boot")):
        uboot_env_path = os.path.join(staging_dir_host, "boot", uboot_env_binary)
        if os.path.exists(uboot_env_path):
            shutil.copy(uboot_env_path, d.getVar("B"))
            bootscr_id = uboot_env_binary
            fitimage_emit_section_boot_script(d, itsfile, bootscr_id, uboot_env_binary)
        else:
            bb.warn("%s not found." % uboot_env_path)

    #
    # Step 4: Prepare a setup section. (For x86)
    #
    setup_bin_path = os.path.join(d.getVar("KERNEL_OUTPUT_DIR"), "setup.bin")
    if os.path.exists(setup_bin_path):
        setupcount = 1
        fitimage_emit_section_setup(d, itsfile, setupcount, setup_bin_path)

    #
    # Step 5: Prepare a ramdisk section.
    #
    if ramdiskcount == 1 and d.getVar("INITRAMFS_IMAGE_BUNDLE") != "1":
        # Find and use the first initramfs image archive type we find
        found = False
        for img in d.getVar("FIT_SUPPORTED_INITRAMFS_FSTYPES").split():
            initramfs_path = os.path.join(d.getVar("DEPLOY_DIR_IMAGE"), "%s.%s" % (d.getVar('INITRAMFS_IMAGE_NAME'), img))
            if os.path.exists(initramfs_path):
                bb.note("Found initramfs image: " + initramfs_path)
                found = True
                fitimage_emit_section_ramdisk(d,itsfile, ramdiskcount, initramfs_path)
                break
            else:
                bb.note("Did not find initramfs image: " + initramfs_path)

        if not found:
            bb.fatal("Could not find a valid initramfs type for %s, the supported types are: %s" % (d.getVar('INITRAMFS_IMAGE_NAME'), d.getVar('FIT_SUPPORTED_INITRAMFS_FSTYPES')))

    fitimage_emit_section_maint(itsfile, "sectend")

    # Force the first Kernel and DTB in the default config
    kernelcount = 1
    if dtbcount:
        dtbcount = 1

    #
    # Step 6: Prepare a configurations section
    #
    fitimage_emit_section_maint(itsfile, "confstart")

    # kernel-fitimage.bbclass currently only supports a single kernel (no less or
    # more) to be added to the FIT image along with 0 or more device trees and
    # 0 or 1 ramdisk.
        # It is also possible to include an initramfs bundle (kernel and rootfs in one binary)
        # When the initramfs bundle is used ramdisk is disabled.
    # If a device tree is to be part of the FIT image, then select
    # the default configuration to be used is based on the dtbcount. If there is
    # no dtb present than select the default configuation to be based on
    # the kernelcount.
    if DTBS:
        for i, DTB in enumerate(DTBS.split(), start=1):
            dtb_ext = os.path.splitext(DTB)[1]
            if dtb_ext == ".dtbo":
                fitimage_emit_section_config(d, itsfile, "", DTB, "", bootscr_id, "", int(i == dtbcount), default_dtb_image)
            else:
                fitimage_emit_section_config(d, itsfile, kernelcount, DTB, ramdiskcount, bootscr_id, setupcount, int(i == dtbcount), default_dtb_image)
    else:
        defaultconfigcount = 1
        fitimage_emit_section_config(d, itsfile, kernelcount, "", ramdiskcount, bootscr_id, setupcount, defaultconfigcount, default_dtb_image)

    fitimage_emit_section_maint(itsfile, "sectend")
    fitimage_emit_section_maint(itsfile, "fitend")

    #
    # Step 7: Assemble the image
    #
    cmd = [
        d.getVar("UBOOT_MKIMAGE"),
        '-f', itsfile,
        os.path.join(d.getVar("KERNEL_OUTPUT_DIR"), fitname)
    ]
    if d.getVar("UBOOT_MKIMAGE_DTCOPTS"):
        cmd.insert(1, '-D')
        cmd.insert(2, d.getVar("UBOOT_MKIMAGE_DTCOPTS"))
    subprocess.run(cmd, check=True)

    #
    # Step 8: Sign the image
    #
    if d.getVar("UBOOT_SIGN_ENABLE") == "1":
        cmd = [
            d.getVar("UBOOT_MKIMAGE_SIGN"),
            '-F',
            '-k', d.getVar("UBOOT_SIGN_KEYDIR"),
            '-r', os.path.join(d.getVar("KERNEL_OUTPUT_DIR"), fitname)
        ]
        if d.getVar("UBOOT_MKIMAGE_DTCOPTS"):
            cmd.extend(['-D', d.getVar("UBOOT_MKIMAGE_DTCOPTS")])
        if d.getVar("UBOOT_MKIMAGE_SIGN_ARGS"):
            cmd.extend(d.getVar("UBOOT_MKIMAGE_SIGN_ARGS").split())
        subprocess.run(cmd, check=True)

python do_assemble_fitimage() {
    if "fitImage" in d.getVar("KERNEL_IMAGETYPES").split():
        os.chdir(d.getVar("B"))
        fitimage_assemble(d, "fit-image.its", "fitImage-none", "")
        if d.getVar("INITRAMFS_IMAGE_BUNDLE") != "1":
            link_name = os.path.join(d.getVar("B"), d.getVar("KERNEL_OUTPUT_DIR"), "fitImage")
            if os.path.islink(link_name):
                os.unlink(link_name)
            os.symlink("fitImage-none", link_name)
}

addtask assemble_fitimage before do_install after do_compile

SYSROOT_DIRS:append = " /sysroot-only"
do_install:append() {
	if echo ${KERNEL_IMAGETYPES} | grep -wq "fitImage" && \
		[ "${UBOOT_SIGN_ENABLE}" = "1" ]; then
		install -D ${B}/${KERNEL_OUTPUT_DIR}/fitImage-none ${D}/sysroot-only/fitImage
	fi
}

python do_assemble_fitimage_initramfs() {
    if "fitImage" in d.getVar("KERNEL_IMAGETYPES").split() and d.getVar("INITRAMFS_IMAGE"):
        os.chdir(d.getVar("B"))
        if d.getVar("INITRAMFS_IMAGE_BUNDLE") == "1":
            fitimage_assemble(d, "fit-image-%s.its" % d.getVar("INITRAMFS_IMAGE"), "fitImage-bundle", "")
            link_name =  os.path.join(d.getVar("B"), d.getVar("KERNEL_OUTPUT_DIR"), "fitImage")
            if os.path.islink(link_name):
                os.unlink(link_name)
            os.symlink("fitImage-bundle", link_name)
        else:
            fitimage_assemble(d, "fit-image-%s.its" % d.getVar("INITRAMFS_IMAGE"), "fitImage-%s" % d.getVar("INITRAMFS_IMAGE"), 1)
}

addtask assemble_fitimage_initramfs before do_deploy after do_bundle_initramfs

do_kernel_generate_rsa_keys() {
	if [ "${UBOOT_SIGN_ENABLE}" = "0" ] && [ "${FIT_GENERATE_KEYS}" = "1" ]; then
		bbwarn "FIT_GENERATE_KEYS is set to 1 even though UBOOT_SIGN_ENABLE is set to 0. The keys will not be generated as they won't be used."
	fi

	if [ "${UBOOT_SIGN_ENABLE}" = "1" ] && [ "${FIT_GENERATE_KEYS}" = "1" ]; then

		# Generate keys to sign configuration nodes, only if they don't already exist
		if [ ! -f "${UBOOT_SIGN_KEYDIR}/${UBOOT_SIGN_KEYNAME}".key ] || \
			[ ! -f "${UBOOT_SIGN_KEYDIR}/${UBOOT_SIGN_KEYNAME}".crt ]; then

			# make directory if it does not already exist
			mkdir -p "${UBOOT_SIGN_KEYDIR}"

			bbnote "Generating RSA private key for signing fitImage"
			openssl genrsa ${FIT_KEY_GENRSA_ARGS} -out \
				"${UBOOT_SIGN_KEYDIR}/${UBOOT_SIGN_KEYNAME}".key \
			"${FIT_SIGN_NUMBITS}"

			bbnote "Generating certificate for signing fitImage"
			openssl req ${FIT_KEY_REQ_ARGS} "${FIT_KEY_SIGN_PKCS}" \
				-key "${UBOOT_SIGN_KEYDIR}/${UBOOT_SIGN_KEYNAME}".key \
				-out "${UBOOT_SIGN_KEYDIR}/${UBOOT_SIGN_KEYNAME}".crt
		fi

		# Generate keys to sign image nodes, only if they don't already exist
		if [ ! -f "${UBOOT_SIGN_KEYDIR}/${UBOOT_SIGN_IMG_KEYNAME}".key ] || \
			[ ! -f "${UBOOT_SIGN_KEYDIR}/${UBOOT_SIGN_IMG_KEYNAME}".crt ]; then

			# make directory if it does not already exist
			mkdir -p "${UBOOT_SIGN_KEYDIR}"

			bbnote "Generating RSA private key for signing fitImage"
			openssl genrsa ${FIT_KEY_GENRSA_ARGS} -out \
				"${UBOOT_SIGN_KEYDIR}/${UBOOT_SIGN_IMG_KEYNAME}".key \
			"${FIT_SIGN_NUMBITS}"

			bbnote "Generating certificate for signing fitImage"
			openssl req ${FIT_KEY_REQ_ARGS} "${FIT_KEY_SIGN_PKCS}" \
				-key "${UBOOT_SIGN_KEYDIR}/${UBOOT_SIGN_IMG_KEYNAME}".key \
				-out "${UBOOT_SIGN_KEYDIR}/${UBOOT_SIGN_IMG_KEYNAME}".crt
		fi
	fi
}

addtask kernel_generate_rsa_keys before do_assemble_fitimage after do_compile

kernel_do_deploy[vardepsexclude] = "DATETIME"
kernel_do_deploy:append() {
	# Update deploy directory
	if echo ${KERNEL_IMAGETYPES} | grep -wq "fitImage"; then

		if [ "${INITRAMFS_IMAGE_BUNDLE}" != "1" ]; then
			bbnote "Copying fit-image.its source file..."
			install -m 0644 ${B}/fit-image.its "$deployDir/fitImage-its-${KERNEL_FIT_NAME}.its"
			if [ -n "${KERNEL_FIT_LINK_NAME}" ] ; then
				ln -snf fitImage-its-${KERNEL_FIT_NAME}.its "$deployDir/fitImage-its-${KERNEL_FIT_LINK_NAME}"
			fi

			bbnote "Copying linux.bin file..."
			install -m 0644 ${B}/linux.bin $deployDir/fitImage-linux.bin-${KERNEL_FIT_NAME}${KERNEL_FIT_BIN_EXT}
			if [ -n "${KERNEL_FIT_LINK_NAME}" ] ; then
				ln -snf fitImage-linux.bin-${KERNEL_FIT_NAME}${KERNEL_FIT_BIN_EXT} "$deployDir/fitImage-linux.bin-${KERNEL_FIT_LINK_NAME}"
			fi
		fi

		if [ -n "${INITRAMFS_IMAGE}" ]; then
			bbnote "Copying fit-image-${INITRAMFS_IMAGE}.its source file..."
			install -m 0644 ${B}/fit-image-${INITRAMFS_IMAGE}.its "$deployDir/fitImage-its-${INITRAMFS_IMAGE_NAME}-${KERNEL_FIT_NAME}.its"
			if [ -n "${KERNEL_FIT_LINK_NAME}" ] ; then
				ln -snf fitImage-its-${INITRAMFS_IMAGE_NAME}-${KERNEL_FIT_NAME}.its "$deployDir/fitImage-its-${INITRAMFS_IMAGE_NAME}-${KERNEL_FIT_LINK_NAME}"
			fi

			if [ "${INITRAMFS_IMAGE_BUNDLE}" != "1" ]; then
				bbnote "Copying fitImage-${INITRAMFS_IMAGE} file..."
				install -m 0644 ${B}/${KERNEL_OUTPUT_DIR}/fitImage-${INITRAMFS_IMAGE} "$deployDir/fitImage-${INITRAMFS_IMAGE_NAME}-${KERNEL_FIT_NAME}${KERNEL_FIT_BIN_EXT}"
				if [ -n "${KERNEL_FIT_LINK_NAME}" ] ; then
					ln -snf fitImage-${INITRAMFS_IMAGE_NAME}-${KERNEL_FIT_NAME}${KERNEL_FIT_BIN_EXT} "$deployDir/fitImage-${INITRAMFS_IMAGE_NAME}-${KERNEL_FIT_LINK_NAME}"
				fi
			fi
		fi
	fi
}
