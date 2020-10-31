DESCRIPTION = "Parses image files’ header and return image size."
HOMEPAGE = "https://github.com/shibukawa/imagesize_py"
SECTION = "devel/python"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE.rst;md5=cc3ed00294f08c93200bc064c73c9d40"

SRC_URI[sha256sum] = "b1f6b5a4eab1f73479a50fb79fcf729514a900c341d8503d62a62dbc4127a2b1"

inherit setuptools3 pypi

BBCLASSEXTEND = "native nativesdk"
