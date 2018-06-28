#
# Copyright (C) 2018 Intel Corporation
#

SUMMARY = "Graphical User Interface testing tools"

PACKAGE_ARCH = "${MACHINE_ARCH}"

inherit packagegroup


RDEPENDS_packagegroup-core-gui-testing = "\
    python3-dogtail"

RRECOMMENDS_packagegroup-core-gui-testing = "\
    "
