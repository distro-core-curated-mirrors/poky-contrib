SUMMARY = "OpenGL driver testing framework"
LICENSE = "MIT & LGPLv2+ & GPLv3 & GPLv2+ & BSD-3-Clause"
LIC_FILES_CHKSUM = "file://COPYING;md5=b2beded7103a3d8a442a2a0391d607b0"

SRC_URI = "git://anongit.freedesktop.org/piglit \
           file://0001-cmake-install-bash-completions-in-the-right-place.patch \
           file://0001-tests-Use-FE_UPWARD-only-if-its-defined-in-fenv.h.patch \
           file://0001-cmake-Link-utils-with-xcb-explicitly.patch \
           file://0001-cmake-Link-test-utils-with-ldl.patch \
           file://piglit.sh \
           "

# From 2016-07-07
SRCREV = "c39e41a86551eb390b8da23232dc8577639403d0"
# (when PV goes above 1.0 remove the trailing r)
PV = "1.0+gitr${SRCPV}"

S = "${WORKDIR}/git"

DEPENDS = "libpng virtual/libx11 libxrender waffle virtual/libgl libglu python3-mako-native python3-numpy-native python3-six-native"

inherit cmake python3native distro_features_check bash-completion
# depends on virtual/libx11
REQUIRED_DISTRO_FEATURES = "x11"

# The built scripts go into the temporary directory according to tempfile
# (typically /tmp) which can race if multiple builds happen on the same machine,
# so tell it to use a directory in ${B} to avoid overwriting.
export TEMP = "${B}/temp/"
do_compile[dirs] =+ "${B}/temp/"

PACKAGECONFIG ??= ""
PACKAGECONFIG[freeglut] = "-DPIGLIT_USE_GLUT=1,-DPIGLIT_USE_GLUT=0,freeglut,"

do_configure_prepend() {
   if [ "${@bb.utils.contains('PACKAGECONFIG', 'freeglut', 'yes', 'no', d)}" = "no" ]; then
        sed -i -e "/^#.*include <GL\/freeglut_ext.h>$/d" ${S}/src/piglit/glut_wrap.h
        sed -i -e "/^#.*include.*<GL\/glut.h>$/d" ${S}/src/piglit/glut_wrap.h
   fi
}

do_install() {
    oe_runmake -C ${B} 'DESTDIR=${D}' install/strip
    mv ${D}${bindir}/piglit ${D}${bindir}/piglit.real
    install -m 755 ${WORKDIR}/piglit.sh ${D}${bindir}/piglit
    tar -C ${D}${libdir}/piglit/ -czf ${D}${libdir}/piglit/generated_tests.tar.gz generated_tests/
}

PACKAGES =+ "${PN}-generated-tests ${PN}-generated-tests-compressed"

RDEPENDS_${PN} = "waffle python3 python3-mako python3-json \
	python3-subprocess python3-misc python3-importlib \
	python3-unixadmin python3-xml python3-multiprocessing \
	python3-six python3-shell python3-io python3-argparse \
	mesa-demos bash \
	"

INSANE_SKIP_${PN} += "dev-so already-stripped"

SUMMARY_${PN}-generated-tests = "Generated piglit tests (multiple GB)"
FILES_${PN}-generated-tests = "${libdir}/piglit/generated_tests/*"
CONFLICTS_${PN}-generated-tests = "${PN}-generated-tests-compressed"
RDEPENDS_${PN}-generated-tests += "tar"

SUMMARY_${PN}-generated-tests-compressed = "Generated piglit tests in compressed archive"
FILES_${PN}-generated-tests-compressed = "${libdir}/piglit/generated_tests.tar.gz"
CONFLICTS_${PN}-generated-tests-compressed = "${PN}-generated-tests"
pkg_postrm_${PN}-generated-tests-compressed () {
    rm -rf $D${libdir}/piglit/generated_tests/
}

