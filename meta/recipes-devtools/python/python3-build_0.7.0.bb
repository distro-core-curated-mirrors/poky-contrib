SUMMARY = "A simple, correct PEP517 package builder"
HOMEPAGE = "https://github.com/pypa/build"
BUGTRACKER = "https://github.com/pypa/build/issues"
CHANGELOG = "https://pypa-build.readthedocs.io/en/stable/changelog.html"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=310439af287b0fb4780b2ad6907c256c"

SRC_URI[sha256sum] = "1aaadcd69338252ade4f7ec1265e1a19184bf916d84c9b7df095f423948cb89f"

inherit pypi setuptools_build_meta

RDEPENDS:${PN} += "python3-core python3-packaging python3-pep517 python3-tomli"

FILES:${PN} += "${PYTHON_SITEPACKAGES_DIR}/bin/pyproject-build"

BBCLASSEXTEND = "native nativesdk"
