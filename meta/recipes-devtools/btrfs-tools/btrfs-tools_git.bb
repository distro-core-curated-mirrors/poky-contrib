SUMMARY = "Checksumming Copy on Write Filesystem utilities"
DESCRIPTION = "Btrfs is a new copy on write filesystem for Linux aimed at \
implementing advanced features while focusing on fault tolerance, repair and \
easy administration. \
This package contains utilities (mkfs, fsck, btrfsctl) used to work with \
btrfs and an utility (btrfs-convert) to make a btrfs filesystem from an ext3."

HOMEPAGE = "https://btrfs.wiki.kernel.org"

LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=fcb02dc552a041dee27e4b85c7396067"
SECTION = "base"
<<<<<<< HEAD
DEPENDS = "util-linux attr e2fsprogs lzo acl"

SRCREV = "194aa4a1bd6447bb545286d0bcb0b0be8204d79f"
SRC_URI = "git://git.kernel.org/pub/scm/linux/kernel/git/mason/btrfs-progs.git"

S = "${WORKDIR}/git"

PV = "0.20+git${SRCPV}"

SRC_URI += "file://weak-defaults.patch"
SRC_URI += "file://btrfs-progs-fix-parallel-build.patch"
SRC_URI += "file://btrfs-progs-fix-parallel-build2.patch"
=======
DEPENDS = "util-linux attr"

SRCREV = "fdb6c0402337d9607c7a39155088eaf033742752"
SRC_URI = "git://git.kernel.org/pub/scm/linux/kernel/git/mason/btrfs-progs.git;protocol=git"

S = "${WORKDIR}/git"

PR = "r6"

SRC_URI += " file://fix_use_of_gcc.patch \
	 file://weak-defaults.patch \
	 file://fix_race_condition_with_multithreaded_make.patch "

SRC_URI[md5sum] = "78b1700d318de8518abfaab71f99a885"
SRC_URI[sha256sum] = "1285774e0cb72984fac158dd046c8d405324754febd30320cd31e459253e4b65"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

do_install () {
	oe_runmake 'DESTDIR=${D}' install
}

BBCLASSEXTEND = "native"
