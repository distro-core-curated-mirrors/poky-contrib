SUMMARY = "A Quart extension to provide trio support"
DESCRIPTION = "Quart-Trio is an extension for Quart to support the Trio \
event loop. This is an alternative to using the asyncio event loop present \
in the Python standard library and supported by default in Quart."
HOMEPAGE = "https://github.com/pgjones/quart-trio"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=8b55b0913488ba6e14df06d407f10691"

SRC_URI[sha256sum] = "02ec840998d0e897eeabc0e5f48c12d8204e91a823870fd0b8b2f7331b44198c"

inherit pypi python_pdm_backend

PYPI_PACKAGE = "quart_trio"
