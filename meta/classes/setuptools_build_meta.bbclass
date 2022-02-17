inherit python3native python3-dir

DEPENDS += "python3 python3-pip-native python3-setuptools-native python3-wheel-native"

SETUPTOOLS_BUILD_META_PACKAGE ?= "${PYPI_PACKAGE}"

do_configure () {
    mkdir -p ${S}/dist
    cat > ${S}/build-it.py << EOF
import os
import sys
from setuptools import build_meta
wheel = build_meta.build_wheel('./dist')
print(wheel, file = sys.stdout)
os.environ["PYPA_WHEEL"] = wheel
EOF 
}

#python do_compile() {
#    import os
#    import sys
#    from setuptools import build_meta
#    wheel = build_meta.build_wheel('./dist')
#    print(wheel, file = sys.stdout)
#    d.setVar('PYPA_WHEEL', wheel)
#    bb.plain( "*************************************" )
#    bb.plain( "do_compile:PYPA_WHEEL = {}".format(d.getVar('PYPA_WHEEL')) )
#    bb.plain( "*************************************" )
#}

do_compile () {
    nativepython3 build-it.py
}

do_install () {
    install -d ${D}${PYTHON_SITEPACKAGES_DIR}
    echo "${@d.getVar('PYPA_WHEEL')}"
    bbplain "*************************************"
    bbplain "do_install:PYPA_WHEEL = ${@d.getVar('PYPA_WHEEL')}"
    bbplain "*************************************"
    PYPA_WHEEL=$(find ./dist -name *.whl)
    nativepython3 -m pip install -vvvv --no-deps --no-index --target ${D}${PYTHON_SITEPACKAGES_DIR} --find-links=${STAGING_DIR}${PYTHON_SITEPACKAGES_DIR} ${PYPA_WHEEL}
    bbplain "SETUPTOOLS_BUILD_META_PACKAGE=${SETUPTOOLS_BUILD_META_PACKAGE}"
}

FILES:${PN} += "\
    ${PYTHON_SITEPACKAGES_DIR}/${SETUPTOOLS_BUILD_META_PACKAGE}/* \
    ${PYTHON_SITEPACKAGES_DIR}/${SETUPTOOLS_BUILD_META_PACKAGE}-${PV}.dist-info/* \
"
