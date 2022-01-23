PYPA_INSTALLER_PACKAGE ?= "${PYPI_PACKAGE}"

DEPENDS += "python3 python3-tomli-native python3-installer-native"

pypa_installer_do_install:prepend() {
    cat > ${S}/install-it.py << EOF
from installer import install
from installer.destinations import SchemeDictionaryDestination
from installer.sources import WheelFile

sysconfig_paths={'stdlib': '${D}${libdir}/${PYTHON_DIR}', 'platstdlib': '${D}${libdir}/${PYTHON_DIR}', 'purelib': '${D}${PYTHON_SITEPACKAGES_DIR}', 'platlib': '${D}${PYTHON_SITEPACKAGES_DIR}', 'include': '${D}${incdir}/${PYTHON_DIR}', 'platinclude': '${D}${incdir}/${PYTHON_DIR}', 'scripts': '${D}${bindir}', 'data': '${D}${exec_prefix}'}

destination = SchemeDictionaryDestination(
    sysconfig_paths,
    interpreter="${STAGING_BINDIR_NATIVE}/python3-native/python3",
    script_kind="posix",
)


with WheelFile.open("dist/${PYPA_INSTALLER_PACKAGE}-${PV}-py2.py3-none-any.whl") as source:
    install(
        source=source,
        destination=destination,
        additional_metadata={
            "INSTALLER": b"python3-installer-0.4.0",
        },
    )
EOF
}

pypa_install_do_install() {
    ${STAGING_BINDIR_NATIVE}/python3-native/python3 ${S}/install-it.py
}
