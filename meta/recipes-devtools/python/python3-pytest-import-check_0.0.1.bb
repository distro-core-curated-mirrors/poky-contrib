SUMMARY = "pytest plugin to check whether Python modules can be imported"
HOMEPAGE = "https://github.com/projg2/pytest-import-check/"
LICENSE = "GPL-2.0-or-later"
# Use proper license text when https://github.com/projg2/pytest-import-check/issues/1 is resolved
LIC_FILES_CHKSUM = "file://pyproject.toml;beginline=10;endline=10;md5=730050c651cb4bb948ff00e73dc8810a"

SRC_URI[sha256sum] = "d0caa74543ee2484e0bc09efa8c1e1b3bd25eead16e2217ff4ffa137195b70cc"

inherit pypi python_flit_core

RDEPENDS:${PN} = "python3-pytest"

BBCLASSEXTEND = "native nativesdk"
