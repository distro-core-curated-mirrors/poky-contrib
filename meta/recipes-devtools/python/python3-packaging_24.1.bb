SUMMARY = "Core utilities for Python packages"
HOMEPAGE = "https://github.com/pypa/packaging"
LICENSE = "Apache-2.0 | BSD-2-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=faadaedca9251a90b205c9167578ce91"

SRC_URI[sha256sum] = "026ed72c8ed3fcce5bf8950572258698927fd1dbda10a5e981cdf0ac37f4f002"

inherit pypi python_flit_core ptest

BBCLASSEXTEND = "native nativesdk"

# Bootstrap the native build
DEPENDS:remove:class-native = "python3-build-native"
RDEPENDS:${PN} += "python3-profile"

do_compile:class-native () {
    python_flit_core_do_manual_build
}

RDEPENDS:${PN}-ptest += "python3-pytest python3-pretend"
INSANE_SKIP:${PN} += "already-stripped"
INSANE_SKIP:${PN}-ptest += "arch"

do_install_ptest() {
    cp -r ${S}/tests ${D}${PTEST_PATH}
    rm -f ${D}${PTEST_PATH}/tests/manylinux/build.sh
}
