SUMMARY = "Snowball compiler and stemming algorithms"
HOMEPAGE = "https://github.com/snowballstem/snowball"

LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://COPYING;md5=2750797da77c1d784e7626b3f7d7ff3e"

SRC_URI[sha256sum] = "df3bac3df4c2c01363f3dd2cfa78cce2840a79b9f1c2d2de9ce8d31683992f52"

PYPI_PACKAGE = "snowballstemmer"

inherit pypi setuptools3

BBCLASSEXTEND = "native nativesdk"
