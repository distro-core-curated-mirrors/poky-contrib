SUMMARY = "Wrappers to build Python packages using PEP 517 hooks"
HOMEPAGE = "https://github.com/pypa/pep517"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=aad69c93f605003e3342b174d9b0708c"

SRC_URI[sha256sum] = "931378d93d11b298cf511dd634cf5ea4cb249a28ef84160b3247ee9afb4e8ab0"

inherit pypi flit_core

DEPENDS += "python3 python3-tomli-native python3-installer-native"

do_install:prepend() {
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

with WheelFile.open("dist/${PYPI_PACKAGE}-${PV}-py2.py3-none-any.whl") as source:
    install(
        source=source,
        destination=destination,
        additional_metadata={
            "INSTALLER": b"python3-installer-0.4.0",
        },
    )
EOF
}

# override flit_core_do_install
do_install() {
    ${STAGING_BINDIR_NATIVE}/python3-native/python3 ${S}/install-it.py
}

RDEPENDS:${PN} = "\
    python3-importlib-metadata \
    python3-toml \
    python3-tomli \
    python3-zipp \
"

RDEPENDS:${PN}:append:class-target = "\
    python3-compression \
    python3-core \
    python3-curses \
    python3-io \
    python3-json \
    python3-logging \
    python3-shell \
    python3-unittest \
"

# WARNING: We were unable to map the following python package/module
# dependencies to the bitbake packages which include them:
#    importlib_metadata
#    mock
#    pytest
#    testpath
#    testpath.tempdir
#    toml
#    tomli
#    zipp

BBCLASSEXTEND = "native nativesdk"
