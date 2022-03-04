inherit pip_install_wheel python3native python3-dir setuptools3-base

DEPENDS += "python3 python3-flit-core-native python3-pip-native"

flit_core_do_compile () {
    nativepython3 -c "from flit_core import buildapi; buildapi.build_wheel('${PIP_INSTALL_DIST_PATH}')"
}
do_compile[cleandirs] += "${PIP_INSTALL_DIST_PATH}"

EXPORT_FUNCTIONS do_compile
