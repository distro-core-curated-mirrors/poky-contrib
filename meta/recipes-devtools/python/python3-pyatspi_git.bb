# Recipe created by recipetool
# This is the basis of a recipe and may need further editing in order to be fully functional.
# (Feel free to remove these comments when editing.)

# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
#
# The following license files were not able to be identified and are
# represented as "Unknown" below, you will need to check them yourself:
#   COPYING
#
# NOTE: multiple licenses have been detected; they have been separated with &
# in the LICENSE value for now since it is a reasonable assumption that all
# of the licenses apply. If instead there is a choice between the multiple
# licenses then you should change the value to separate the licenses with |
# instead of &. If there is any doubt, check the accompanying documentation
# to determine which situation is applicable.
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=e9f288ba982d60518f375b5898283886 \
                    file://COPYING.GPL;md5=751419260aa954499f7abaabaa882bbe"

SRC_URI = "git://github.com/GNOME/pyatspi2.git;protocol=https"

# Modify these as desired
PV = "2.31.1+git${SRCPV}"
SRCREV = "a91590165daf634cf90df86bf30d6490c8a62b5b"

S = "${WORKDIR}/git"

# NOTE: unable to map the following pkg-config dependencies: gtk+-2.0
#       (this is based on recipes that have previously been built and packaged)
DEPENDS = "dbus-glib python3-pygobject python3-dbus-native gtk+ libx11 glib-2.0 libxml2 at-spi2-atk dbus"
RDEPENDS_${PN} += "dbus-glib python3-pygobject python3-dbus gtk+ libx11 glib-2.0 libxml2 at-spi2-atk dbus"

# NOTE: if this software is not capable of being built in a separate build directory
# from the source, you should replace autotools with autotools-brokensep in the
# inherit line
inherit pkgconfig python3native autotools ptest

# Specify any options you want to pass to the configure script using EXTRA_OECONF:
EXTRA_OECONF = "--enable-tests"

FILES_${PN} += "${PYTHON_SITEPACKAGES_DIR}/pyatspi/*"

