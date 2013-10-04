#
# Copyright (C) 2010 Intel Corporation
#

SUMMARY = "Self-hosting"
DESCRIPTION = "Packages required to run the build system"
<<<<<<< HEAD
PR = "r13"
=======
PR = "r12"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
LICENSE = "MIT"

inherit packagegroup

PACKAGES = "\
    packagegroup-self-hosted \
    packagegroup-self-hosted-debug \
    packagegroup-self-hosted-sdk \
    packagegroup-self-hosted-extended \
    packagegroup-self-hosted-graphics \
    packagegroup-self-hosted-host-tools \
    "

RDEPENDS_packagegroup-self-hosted = "\
    packagegroup-self-hosted-debug \
    packagegroup-self-hosted-sdk \
    packagegroup-self-hosted-extended \
    packagegroup-self-hosted-graphics \
    packagegroup-self-hosted-host-tools \
    "

RDEPENDS_packagegroup-self-hosted-host-tools = "\
    connman \
    connman-plugin-ethernet \
    dhcp-client \
    e2fsprogs \
    e2fsprogs-e2fsck \
    e2fsprogs-mke2fs \
    e2fsprogs-tune2fs \
    genext2fs \
    hdparm \
    iptables \
    lsb \
<<<<<<< HEAD
    xdg-utils \
    mc \
    mc-fish \
    mc-helpers \
    mc-helpers-perl \
    mc-helpers-python \
    midori \
    pcmanfm \
=======
    mc \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    parted \
    pseudo \
    screen \
    vte \
    "

RRECOMMENDS_packagegroup-self-hosted-host-tools = "\
    kernel-module-tun \
    kernel-module-iptable-raw \
    kernel-module-iptable-nat \
    kernel-module-iptable-mangle \
    kernel-module-iptable-filter \
	"

# eglibc-utils: for rpcgen
RDEPENDS_packagegroup-self-hosted-sdk = "\
    autoconf \
    automake \
    binutils \
    binutils-symlinks \
    ccache \
    coreutils \
    cpp \
    cpp-symlinks \
    distcc \
    eglibc-utils \
    eglibc-gconv-ibm850 \
    file \
    findutils \
    g++ \
    g++-symlinks \
    gcc \
    gcc-symlinks \
    intltool \
    ldd \
    less \
<<<<<<< HEAD
    libssp \
    libssp-dev \
    libssp-staticdev \
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    libstdc++ \
    libstdc++-dev \
    libtool \
    make \
    mktemp \
    perl-module-re \
    perl-module-text-wrap \
    pkgconfig \
    quilt \
    sed \
    "

RDEPENDS_packagegroup-self-hosted-debug = " \
    gdb \
    gdbserver \
    rsync \
    strace \
    tcf-agent"


RDEPENDS_packagegroup-self-hosted-extended = "\
    bzip2 \
    chkconfig \
    chrpath \
    cpio \
    curl \
    diffstat \
    diffutils \
    elfutils \
    expat \
    gamin \
    gawk \
    gdbm \
    gettext \
    gettext-runtime \
    git \
    grep \
    groff \
    gzip \
<<<<<<< HEAD
    settings-daemon \
    hicolor-icon-theme \
    sato-icon-theme \
=======
    hicolor-icon-theme \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    libaio \
    libusb1 \
    libxml2 \
    lrzsz \
    lsof \
    lzo \
    man \
    man-pages \
    mdadm \
    minicom \
    mtools \
    ncurses \
<<<<<<< HEAD
    ncurses-terminfo-base \
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    neon \
    nfs-utils \
    nfs-utils-client \
    openssl \
<<<<<<< HEAD
    openssh-sftp-server \
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    opkg \
    opkg-utils \
    patch \
    perl \
    perl-dev \
    perl-modules \
    perl-pod \
    ${PTH} \
    python \
    python-compile \
    python-compiler \
    python-compression \
    python-core \
    python-curses \
    python-datetime \
<<<<<<< HEAD
    python-difflib \
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    python-distutils \
    python-elementtree \
    python-email \
    python-fcntl \
<<<<<<< HEAD
    python-git \
    python-json \
    python-logging \
    python-misc \
    python-mmap \
=======
    python-logging \
    python-misc \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    python-multiprocessing \
    python-netclient \
    python-netserver \
    python-pickle \
    python-pkgutil \
<<<<<<< HEAD
    python-pprint \
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    python-re \
    python-rpm \
    python-shell \
    python-sqlite3 \
    python-subprocess \
    python-textutils \
<<<<<<< HEAD
    python-unittest \
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    python-unixadmin \
    python-xmlrpc \
    quota \
    readline \
    rpm \
    setserial \
    socat \
    subversion \
    sudo \
    sysstat \
    tar \
    tcl \
    texi2html \
    texinfo \
    unzip \
    usbutils \
    watchdog \
    wget \
    which \
    xinetd \
    zip \
    zlib \
    "


RDEPENDS_packagegroup-self-hosted-graphics = "\
    builder \
    libgl \
    libgl-dev \
    libglu \
    libglu-dev \
    libsdl \
    libsdl-dev \
    libx11-dev \
    python-pygtk \
    gtk-theme-clearlooks \
    "
PTH = "pth"
PTH_libc-uclibc = ""
