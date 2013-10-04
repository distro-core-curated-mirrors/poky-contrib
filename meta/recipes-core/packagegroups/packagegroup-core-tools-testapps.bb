#
# Copyright (C) 2008 OpenedHand Ltd.
#

SUMMARY = "Testing tools/applications"
LICENSE = "MIT"

<<<<<<< HEAD
PR = "r2"
=======
PR = "r1"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

inherit packagegroup

PACKAGE_ARCH = "${MACHINE_ARCH}"

# For backwards compatibility after rename
RPROVIDES_${PN} = "task-core-tools-testapps"
RREPLACES_${PN} = "task-core-tools-testapps"
RCONFLICTS_${PN} = "task-core-tools-testapps"

# kexec-tools doesn't work on Mips
KEXECTOOLS ?= "kexec"
KEXECTOOLS_mips ?= ""
KEXECTOOLS_mipsel ?= ""
KEXECTOOLS_powerpc ?= ""
KEXECTOOLS_e5500-64b ?= ""
KEXECTOOLS_aarch64 ?= ""

<<<<<<< HEAD
X11TOOLS = "\
    fstests \
    owl-video \
    mesa-demos \
    x11perf \
    xrestop \
    xwininfo \
    xprop \
    xvideo-tests \
    "

RDEPENDS_${PN} = "\
    blktool \
=======
RDEPENDS_${PN} = "\
    blktool \
    fstests \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    tslib-calibrate \
    tslib-tests \
    lrzsz \
    ${KEXECTOOLS} \
    alsa-utils-amixer \
    alsa-utils-aplay \
<<<<<<< HEAD
    gst-meta-video \
    gst-meta-audio \
    ltp \
    connman-client \
    ${@base_contains('DISTRO_FEATURES', 'x11', "${X11TOOLS}", "", d)} \
=======
    owl-video \
    gst-meta-video \
    gst-meta-audio \
    mesa-demos \
    x11perf \
    xrestop \
    xwininfo \
    xprop \
    xvideo-tests \
    clutter-box2d \
    ltp \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    "
