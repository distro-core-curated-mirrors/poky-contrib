#
# Copyright (C) 2010  Intel Corporation. All rights reserved
#

DESCRIPTION = "Qt package groups"
LICENSE = "MIT"
PR = "r4"

<<<<<<< HEAD
# Qt4 could NOT be built on MIPS64 with 64 bits userspace
COMPATIBLE_HOST_mips64 = "mips64.*-linux-gnun32"

=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
inherit packagegroup

PACKAGES = "${PN}-demoapps"

# For backwards compatibility after rename
RPROVIDES_${PN}-demoapps = "task-core-qt-demos"
RREPLACES_${PN}-demoapps = "task-core-qt-demos"
RCONFLICTS_${PN}-demoapps = "task-core-qt-demos"

QTDEMOS ?= "quicky ${COMMERCIAL_QT} fotowall"

SUMMARY_${PN}-demoapps = "Qt demo applications"
RDEPENDS_${PN}-demoapps = "${QTDEMOS}"
