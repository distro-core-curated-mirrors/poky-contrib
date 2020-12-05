SUMMARY = "A simple, correct PEP517 package builder"
DESCRIPTION = "build will invoke the PEP 517 hooks to build a distribution \
package. It is a simple build tool and does not perform any dependency \
management."
HOMEPAGE = "https://github.com/pypa/build"
SECTION = "devel/python"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=310439af287b0fb4780b2ad6907c256c"

#SRC_URI = "https://files.pythonhosted.org/packages/73/d2/983036d667b6310d9a8db2c14bb515b3904cdbe3c717a2f8019efca1e370/build-${PV}.tar.gz"
SRC_URI[sha256sum] = "08b2b58098ff617d1154056c79f8a70beed18f7cfa710bca23a072196910d5b4"
SRC_URI[sha384sum] = "646f0a7d9ff735339aff584a12614f3c3c0a1a45bec37ae02455268fe151f6c6ce3f0de73504d3b09ab99da89c33ae7b"
SRC_URI[sha512sum] = "23d40fa9d037ff4ba640ece9c38d4a47d28a7640df71f6647b7018a7d8fb63b00924cb3e412d04a84130de52e0ed7cfa8bb118f9c87ed15c6b0958c6cc0bfca9"

S = "${WORKDIR}/build-${PV}"

inherit pypi setuptools3

RDEPENDS_${PN} += "python3-core python3-packaging python3-pep517 python3-toml python3-venv"

BBCLASSEXTEND = "native nativesdk"
