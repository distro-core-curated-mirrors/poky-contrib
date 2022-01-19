SUMMARY = "A library for installing Python wheels."
DESCRIPTION = "This is a low-level library for installing a Python package \
from a wheel distribution. It provides basic functionality and abstractions \
for handling wheels and installing packages from wheels.\
\
* Logic for 'unpacking' a wheel (i.e. installation).\
* Abstractions for various parts of the unpacking process.\
* Extensible simple implementations of the abstractions.\
* Platform-independent Python script wrapper generation."
HOMEPAGE = "https://github.com/pradyunsg/installer"
BUGTRACKER = "https://github.com/pradyunsg/installer/issues"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=5038641aec7a77451e31da828ebfae00"

SRC_URI[sha256sum] = "17d7ca174039fbd85f268e16042e3132ebb03d91e1bbe0f63b9ec6b40619414a"

inherit pypi flit_core

RDEPENDS:${PN} += "python3-core"

# WARNING: We were unable to map the following python package/module
# dependencies to the bitbake packages which include them:
#    nox

BBCLASSEXTEND = "native nativesdk"
