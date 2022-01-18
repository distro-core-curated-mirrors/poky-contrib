inherit python3native python3-dir

DEPENDS += "python3 python3-flit-core-native python3-pip-native"

FLIT_CORE_PACKAGE ?= "${PYPI_PACKAGE}"

do_configure () {
    mkdir -p ${S}/dist
    cat > ${S}/build-it.py << EOF
from flit_core import buildapi
buildapi.build_wheel('./dist')
EOF 
}

do_compile () {
    ${STAGING_BINDIR_NATIVE}/${PYTHON_PN}-native/${PYTHON_PN} ${S}/build-it.py
}

do_install () {
    install -d ${D}${PYTHON_SITEPACKAGES_DIR}
    nativepython3 -m pip install -vvvv --no-deps --no-index --target ${D}${PYTHON_SITEPACKAGES_DIR} --find-links=${STAGING_LIBDIR}/${PYTHON_DIR}/site-packages ./dist/${FLIT_CORE_PACKAGE}-${PV}-*.whl
}

FILES:${PN} += "\
    ${PYTHON_SITEPACKAGES_DIR}/${FLIT_CORE_PACKAGE}/* \
    ${PYTHON_SITEPACKAGES_DIR}/${FLIT_CORE_PACKAGE}-${PV}.dist-info/* \
"
