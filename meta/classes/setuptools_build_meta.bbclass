inherit python3native python3-dir

DEPENDS += "python3 python3-pip-native python3-setuptools-native python3-wheel-native"

SETUPTOOLS_BUILD_META_PACKAGE ?= "${PYPI_PACKAGE}"

do_configure () {
    mkdir -p ${S}/dist
    cat > ${S}/build-it.py << EOF
from setuptools import build_meta
wheel = build_meta.build_wheel('./dist')
print(wheel)
EOF 
}

do_compile () {
    ${STAGING_BINDIR_NATIVE}/${PYTHON_PN}-native/${PYTHON_PN} ${S}/build-it.py
}

do_install () {
    install -d ${D}${PYTHON_SITEPACKAGES_DIR}
    nativepython3 -m pip install -vvvv --no-index --target ${D}${PYTHON_SITEPACKAGES_DIR} --find-links=${STAGING_DIR}${PYTHON_SITEPACKAGES_DIR} ./dist/${SETUPTOOLS_BUILD_META_PACKAGE}-${PV}-*.whl
}

FILES:${PN} += "\
    ${PYTHON_SITEPACKAGES_DIR}/${SETUPTOOLS_BUILD_META_PACKAGE}/* \
    ${PYTHON_SITEPACKAGES_DIR}/${SETUPTOOLS_BUILD_META_PACKAGE}-${PV}.dist-info/* \
"
