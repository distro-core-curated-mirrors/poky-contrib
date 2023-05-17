BPN = "qemu"

require qemu.inc

inherit native

PACKAGECONFIG ??= "user-targets pie"
