inherit pip_install_wheel setuptools3-base

DEPENDS += "python3 python3-setuptools-native python3-wheel-native"

setuptools_build_meta_do_configure () {
    mkdir -p ${S}/dist
    cat > ${S}/build-it.py << EOF
from setuptools import build_meta
wheel = build_meta.build_wheel('${PIP_INSTALL_DIST_PATH}')
print(wheel)
EOF
}

setuptools_build_meta_do_compile () {
    nativepython3 ${S}/build-it.py
}
do_compile[cleandirs] += "${PIP_INSTALL_DIST_PATH}"

EXPORT_FUNCTIONS do_configure do_compile
