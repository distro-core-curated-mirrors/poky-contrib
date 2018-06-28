# Recipe created by recipetool
# This is the basis of a recipe and may need further editing in order to be fully functional.
# (Feel free to remove these comments when editing.)

HOMEPAGE = "https://gitlab.com/dogtail/dogtail/"
# WARNING: the following LICENSE and LIC_FILES_CHKSUM values are best guesses - it is
# your responsibility to verify that the values are complete and correct.
#
# The following license files were not able to be identified and are
# represented as "Unknown" below, you will need to check them yourself:
#   examples/COPYING
#
# NOTE: multiple licenses have been detected; they have been separated with &
# in the LICENSE value for now since it is a reasonable assumption that all
# of the licenses apply. If instead there is a choice between the multiple
# licenses then you should change the value to separate the licenses with |
# instead of &. If there is any doubt, check the accompanying documentation
# to determine which situation is applicable.
LICENSE = "GPLv2 & PD"
LIC_FILES_CHKSUM = "file://COPYING;md5=eb723b61539feef013de476e68b5c50a \
                    file://examples/COPYING;md5=e012ede43b30fda895555797c3ef4b55"

SRC_URI = "git://gitlab.com/dogtail/dogtail.git;protocol=https \
           file://run-ptest \
"

# Modify these as desired
PV = "0.9.11+git${SRCPV}"
SRCREV = "c2c1ef0d6f3ebd0e6c3c79d4ef3533043811dbed"

S = "${WORKDIR}/git"

inherit setuptools3 ptest

# WARNING: the following rdepends are determined through basic analysis of the
# python sources, and might not be 100% accurate.
RDEPENDS_${PN} += " \
    glib-2.0-dev \
    gnome-icon-theme \
    python3-codecs \
    python3-core \
    python3-io \
    python3-math \
    python3-pyatspi \
    python3-pycairo \
    python3-pygobject \
    python3-shell \
    tzdata \
"

do_install_append() {
     sed -i -e '1s|^#!.*|#!/usr/bin/env python3|' ${D}/${bindir}/dogtail-*
     sed -i -e '1s|^#!.*|#!/usr/bin/env python3|' ${D}/${bindir}/sniff
}

RDEPENDS_${PN}-ptest += "gsettings-desktop-schemas python3-nose"

do_install_ptest() {
    install -d ${D}${PTEST_PATH}/tests
    cp -rf ${S}/tests/* ${D}${PTEST_PATH}/tests/
}

# WARNING: We were unable to map the following python package/module
# dependencies to the bitbake packages which include them:
#    Accessibility
#    apt_pkg (distro)
#    cairo
#    conaryclient (distro)
#    gi
#    gi.repository
#    gi.repository.Gio
#    portage (distro)
#    pyatspi
#    rpm (distro)

FILES_${PN} += " \
  /usr/share/icons \
  /usr/share/dogtail \
  /usr/share/icons/hicolor \
  /usr/share/icons/hicolor/scalable \
  /usr/share/icons/hicolor/scalable/apps \
  /usr/share/icons/hicolor/scalable/apps/dogtail-head.svg \
  /usr/share/icons/hicolor/scalable/apps/dogtail-tail.svg \
  /usr/share/dogtail/icons \
  /usr/share/dogtail/glade \
  /usr/share/dogtail/icons/table.xpm \
  /usr/share/dogtail/icons/tree.xpm \
  /usr/share/dogtail/icons/notebook.xpm \
  /usr/share/dogtail/icons/statusbar.xpm \
  /usr/share/dogtail/icons/text.xpm \
  /usr/share/dogtail/icons/scrolledwindow.xpm \
  /usr/share/dogtail/icons/menuitem.xpm \
  /usr/share/dogtail/icons/combo.xpm \
  /usr/share/dogtail/icons/viewport.xpm \
  /usr/share/dogtail/icons/label.xpm \
  /usr/share/dogtail/icons/checkbutton.xpm \
  /usr/share/dogtail/icons/vseparator.xpm \
  /usr/share/dogtail/icons/menubar.xpm \
  /usr/share/dogtail/icons/checkmenuitem.xpm \
  /usr/share/dogtail/icons/spinbutton.xpm \
  /usr/share/dogtail/icons/dialog.xpm \
  /usr/share/dogtail/icons/window.xpm \
  /usr/share/dogtail/icons/toolbar.xpm \
  /usr/share/dogtail/icons/unknown.xpm \
  /usr/share/dogtail/icons/treeitem.xpm \
  /usr/share/dogtail/icons/vscrollbar.xpm \
  /usr/share/dogtail/icons/image.xpm \
  /usr/share/dogtail/icons/colorselection.xpm \
  /usr/share/dogtail/icons/button.xpm \
  /usr/share/dogtail/glade/sniff.ui \
"

INSANE_SKIP_${PN} += "dev-deps"
