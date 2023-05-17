BPN = "qemu"

require qemu-native.inc

EXTRA_OECONF:append = " --target-list=${@get_qemu_usermode_target_list(d)} --disable-install-blobs"

PACKAGECONFIG ??= "pie"
