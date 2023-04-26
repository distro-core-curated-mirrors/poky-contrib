SUMMARY = "asyncio library for communicating with QEMU Monitor Protocol (QMP) servers"
LICENSE = "LGPLv2+ & GPLv2"
LIC_FILES_CHKSUM = "file://LICENSE;md5=4cf66a4984120007c9881cc871cf49db \
                    file://LICENSE_GPL2;md5=441c28d2cf86e15a37fa47e15a72fbac"

SRC_URI[sha256sum] = "c918e9e3ae09abdf70c7ece67637a93ac4583d940bbf48d24ff77987f74f1b8b"

inherit pypi python_setuptools_build_meta

PYPI_PACKAGE = "qemu.qmp"

DEPENDS += "python3-setuptools-scm-native"

BBCLASSEXTEND = "native nativesdk"
