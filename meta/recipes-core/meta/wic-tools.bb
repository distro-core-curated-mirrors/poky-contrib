SUMMARY = "A meta recipe to build native tools used by wic."

LICENSE = "MIT"

DEPENDS = "parted-native syslinux-native gptfdisk-native dosfstools-native mtools-native bmap-tools-native grub-efi-native cdrtools-native"
DEPENDS_append_x86 = " syslinux"
DEPENDS_append_x86-64 = " syslinux"

INHIBIT_DEFAULT_DEPS = "1"
inherit nopackages

python do_build_sysroot () {
    bb.build.exec_func("extend_recipe_sysroot", d)
}
addtask do_build_sysroot after do_prepare_recipe_sysroot before do_build
