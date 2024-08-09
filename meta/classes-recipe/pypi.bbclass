#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

def pypi_package(d):
    bpn = d.getVar('BPN')
    if bpn.startswith('python-'):
        return bpn[7:]
    elif bpn.startswith('python3-'):
        return bpn[8:]
    return bpn

def pypi_normalize(s):
    # As per https://packaging.python.org/en/latest/specifications/binary-distribution-format/#escaping-and-unicode
    import re
    return re.sub(r"[-_.]+", "_", s).lower()

# The PyPI package name (defaults to PN without the python3- prefix)
PYPI_PACKAGE ?= "${@pypi_package(d)}"
# The name of the sdist (rename to PYPI_SDIST_NAME?) TODO is this actually needed?
PYPI_ARCHIVE_NAME ?= "${@pypi_normalize(d.getVar("PYPI_PACKAGE"))}"
# The file extension of the source archive
PYPI_PACKAGE_EXT ?= "tar.gz"
# An optional prefix for the download file in the case of name collisions
PYPI_ARCHIVE_NAME_PREFIX ?= ""

def pypi_src_uri(d):
    """
    Construct a source URL as per https://warehouse.pypa.io/api-reference/integration-guide.html#predictable-urls.
    """
    sdist = d.getVar('PYPI_ARCHIVE_NAME')
    archive_name = d.expand('${PYPI_ARCHIVE_NAME}-${PV}.${PYPI_PACKAGE_EXT}')
    archive_downloadname = d.getVar('PYPI_ARCHIVE_NAME_PREFIX') + archive_name
    return 'https://files.pythonhosted.org/packages/source/%s/%s/%s;downloadfilename=%s' % (sdist[0], sdist, archive_name, archive_downloadname)

PYPI_SRC_URI ?= "${@pypi_src_uri(d)}"

HOMEPAGE ?= "https://pypi.python.org/pypi/${PYPI_PACKAGE}/"
SECTION = "devel/python"
SRC_URI:prepend = "${PYPI_SRC_URI} "
S = "${WORKDIR}/${PYPI_ARCHIVE_NAME}-${PV}"

# Replace any '_' characters in the pypi URI with '-'s to follow the PyPi website naming conventions
# TODO is this still needed? Use API?
UPSTREAM_CHECK_PYPI_PACKAGE ?= "${@d.getVar('PYPI_PACKAGE').replace('_', '-')}"
UPSTREAM_CHECK_URI ?= "https://pypi.org/project/${UPSTREAM_CHECK_PYPI_PACKAGE}/"
UPSTREAM_CHECK_REGEX ?= "/${UPSTREAM_CHECK_PYPI_PACKAGE}/(?P<pver>(\d+[\.\-_]*)+)/"

CVE_PRODUCT ?= "python:${PYPI_PACKAGE}"

# TODO if OE supports it embed the version, ie Provides: bar (= 1.0)
# If OE doesn't support it then we can't use virtual names and instead will
# need to maintain a map of pypi package to oe package (like solibs)
RPROVIDES:${PN}:append = "python-module-${PYPI_PACKAGE}"
