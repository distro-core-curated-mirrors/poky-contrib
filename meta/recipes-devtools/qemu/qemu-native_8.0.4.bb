BPN = "qemu"

require qemu.inc

inherit native

EXTRA_OECONF:append = " --disable-install-blobs"

PACKAGECONFIG ??= "user-targets pie"
