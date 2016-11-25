PRIOTASKS = " \
    mfpr-native \
    gmp-native \
    libmpc-native \
    m4-native \
    autoconf-native \
    automake-native \
    linux-libc-headers \
    glibc-initial \
    glibc \
    libgcc-initial \
    libgcc \
    gcc-runtime \
    expat \
    gettext \
    mesa \
    dbus \
    glib-2.0 \
    libx11 \
    libepoxy \
    xserver-xorg \
    binutils-cross-${TARGET_ARCH} \
    gcc-cross-${TARGET_ARCH} \
    gcc-cross-initial-${TARGET_ARCH} \
    libtool-cross \
    libtool-native \
"

python () {
    for pn in d.getVar("PRIOTASKS").split():
        for task in ["configure", "compile", "install", "populate_sysroot"]:
            d.setVar("BB_TASK_NICE_LEVEL_task-%s_pn-%s" % (task, pn), "0")
            d.setVar("BB_TASK_IONICE_LEVEL_task-%s_pn-%s" % (task, pn), "2.0")
}
