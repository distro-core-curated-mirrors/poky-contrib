BBCLASSEXTEND = "nativesdk"

require qemu.inc

CFLAGS += "${@bb.utils.contains('DISTRO_FEATURES', 'x11', '', '-DEGL_NO_X11=1', d)}"

RDEPENDS:${PN}-common:class-target += "bash"

PACKAGECONFIG ??= " \
    all-targets firmware \
    fdt sdl kvm pie slirp tpm keyring tools guest-agent png \
    ${@bb.utils.filter('DISTRO_FEATURES', 'alsa xen', d)} \
    ${@bb.utils.contains('DISTRO_FEATURES', 'opengl', 'virglrenderer epoxy', '', d)} \
    ${@bb.utils.filter('DISTRO_FEATURES', 'seccomp', d)} \
"
