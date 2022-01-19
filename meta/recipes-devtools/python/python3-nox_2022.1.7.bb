SUMMARY = "nox is a command-line tool that automates testing, similar to tox."
DESCRIPTION = "nox is a command-line tool that automates testing in multiple \
Python environments, similar to tox. Unlike tox, Nox uses a standard Python \
file for configuration."
HOMEPAGE = "https://nox.thea.codes/"
BUGTRACKER ="https://github.com/theacodes/nox/issues"

LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=86d3f3a95c324c9479bd8986968f4327"

SRC_URI[sha256sum] = "b375238cebb0b9df2fab74b8d0ce1a50cd80df60ca2e13f38f539454fcd97d7e"

inherit pypi

DEPENDS += "python3-build-native python3-setuptools-native"

# NOTE: no Makefile found, unable to determine what needs to be done

do_configure () {
	# Specify any needed configure commands here
	:
}

do_compile () {
	# Specify compilation commands here
	:
}

do_install () {
	# Specify install commands here
	:
}

