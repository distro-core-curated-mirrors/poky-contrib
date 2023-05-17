BPN = "qemu"

require qemu.inc

inherit native

EXTRA_OECONF:append = " --disable-tools --disable-install-blobs --disable-guest-agent"

PACKAGECONFIG ??= "user-targets pie"
