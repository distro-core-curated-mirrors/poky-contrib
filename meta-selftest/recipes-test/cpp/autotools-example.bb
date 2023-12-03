#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

SUMMARY = "A C++ example compiled with autotools."

require cpp-example.inc

DEPENDS += "autoconf-archive-native"

SRC_URI += "\
    file://configure.ac \
    file://Makefile.am \
"

inherit autotools

FILES:${PN}-ptest += "${bindir}/test-autotools-example"
