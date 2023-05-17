BPN = "qemu"

inherit python3-dir

require qemu.inc

inherit native

# As some of the files installed by qemu-native and qemu-system-native
# are the same, we depend on qemu-native to get the full installation set
# and avoid file clashes
DEPENDS = "glib-2.0-native zlib-native pixman-native qemu-native bison-native meson-native ninja-native"


PACKAGECONFIG ??= "system-targets fdt alsa kvm pie slirp \
    ${@bb.utils.contains('DISTRO_FEATURES', 'opengl', 'virglrenderer epoxy', '', d)} \
"

do_install:append() {
    install -Dm 0755 ${WORKDIR}/powerpc_rom.bin ${D}${datadir}/qemu

    # The following is also installed by qemu-native
    rm -f ${D}${datadir}/qemu/trace-events-all
    rm -rf ${D}${datadir}/qemu/keymaps
    rm -rf ${D}${datadir}/icons/
    rm -rf ${D}${includedir}/qemu-plugin.h

    # Install qmp.py to be used with testimage
    install -d ${D}${libdir}/qemu-python/qmp/
    install -D ${S}/python/qemu/qmp/* ${D}${libdir}/qemu-python/qmp/
}
