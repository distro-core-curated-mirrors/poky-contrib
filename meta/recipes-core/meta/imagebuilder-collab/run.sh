#!/bin/sh

NATIVESYSROOT=/home/ed/poky/sysroots/x86_64-linux/usr
PATH=$NATIVESYSROOT/bin:$NATIVESYSROOT/sbin:$NATIVESYSROOT/bin/python-native:$PATH \
BBPATH=meta \
PSEUDO_PREFIX=$NATIVESYSROOT \
PSEUDO_LOCALSTATEDIR=`pwd`/tmp/work/-oe-linux/core-image-minimal/1.0-r0/pseudo/ \
PSEUDO_PASSWD=`pwd`/tmp/work/-oe-linux/core-image-minimal/1.0-r0/rootfs \
PSEUDO_NOSYMLINKEXP=1 \
PSEUDO_BINDIR=$NATIVESYSROOT/bin \
PSEUDO_LIBDIR=$NATIVESYSROOT/lib/pseudo/lib \
IMAGE_PKGTYPE="rpm" \
DEPLOY_DIR_IPK="/media/build1/poky/build1/tmp/deploy/ipk" \
DEPLOY_DIR_RPM="/media/build1/poky/build1/tmp/deploy/rpm" \
PACKAGE_ARCHS="all any noarch x86 i586 qemux86" \
ALL_MULTILIB_PACKAGE_ARCHS="all any noarch x86 i586 qemux86" \
COREBASE="/media/build1/poky" \
BUILDNAME="dummyname" \
$NATIVESYSROOT/bin/pseudo ./bitbake/bin/build-rootfs ./meta/core-image-minimal.bb

