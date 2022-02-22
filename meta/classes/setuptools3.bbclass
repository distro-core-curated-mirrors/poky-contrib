inherit setuptools3-base pip_install_wheel

# bdist_wheel builds in ./dist
#B = "${WORKDIR}/build"

SETUPTOOLS_BUILD_ARGS ?= ""
SETUPTOOLS_INSTALL_ARGS ?= "--root=${D} \
    --prefix=${prefix} \
    --install-lib=${PYTHON_SITEPACKAGES_DIR} \
    --install-data=${datadir}"

SETUPTOOLS_PYTHON = "python3"
SETUPTOOLS_PYTHON:class-native = "nativepython3"

SETUPTOOLS_SETUP_PATH ?= "${S}"

setuptools3_do_configure() {
    :
}

def check_for_pyprojecttoml_build_backend():
    import os
    import tomli
    from pathlib import Path
    
    pyprojecttoml_file = Path( 'pyproject.toml')
    bb.plain("pyproject.toml found")
    if pyprojecttoml_file:
        pyprojecttoml_dict = tomli.loads(pyprojecttoml_file) 
        build_system = pyprojecttoml_dict["build-system"] 
        if build_system: 
            bb.plain("[build-system] found in pyproject.toml")
            backend = build_system.key('build_backend')
            if backend == "flit_core.buildapi":
                bb.warn("The source has a pyproject.toml which declares 'flit_core.buildapi' as a build backend, please consider 'inherit flit_core' instead of inheriting setuptools3.")
            elif backend == "setuptools.build_meta":
                bb.warn("The source has a pyproject.toml which declares 'setuptools.build_meta' as a build backend, please consider 'inherit setuptools_build_meta' instead of inheriting setuptools3.")
            else:
                bb.warn("The source has a pyproject.toml which declares '{backend}' as a build backend, but this is not currently supported in oe-core.".format(backend))

python () {
    check_for_pyprojecttoml_build_backend
}

setuptools3_do_compile() {
        cd ${SETUPTOOLS_SETUP_PATH}
        NO_FETCH_BUILD=1 \
        STAGING_INCDIR=${STAGING_INCDIR} \
        STAGING_LIBDIR=${STAGING_LIBDIR} \
        ${STAGING_BINDIR_NATIVE}/${PYTHON_PN}-native/${PYTHON_PN} setup.py \
        bdist_wheel ${SETUPTOOLS_BUILD_ARGS} || \
        bbfatal_log "'${PYTHON_PN} setup.py bdist_wheel ${SETUPTOOLS_BUILD_ARGS}' execution failed."
}
setuptools3_do_compile[vardepsexclude] = "MACHINE"

setuptools3_do_install() {
        cd ${SETUPTOOLS_SETUP_PATH}

        pip_install_wheel_do_install

        # support filenames with *spaces*
        find ${D} -name "*.py" -exec grep -q ${D} {} \; \
                               -exec sed -i -e s:${D}::g {} \;

        for i in ${D}${bindir}/* ${D}${sbindir}/*; do
            if [ -f "$i" ]; then
                sed -i -e s:${PYTHON}:${USRBINPATH}/env\ ${SETUPTOOLS_PYTHON}:g $i
                sed -i -e s:${STAGING_BINDIR_NATIVE}:${bindir}:g $i
            fi
        done

        rm -f ${D}${PYTHON_SITEPACKAGES_DIR}/easy-install.pth

        #
        # FIXME: Bandaid against wrong datadir computation
        #
        if [ -e ${D}${datadir}/share ]; then
            mv -f ${D}${datadir}/share/* ${D}${datadir}/
            rmdir ${D}${datadir}/share
        fi
}
setuptools3_do_install[vardepsexclude] = "MACHINE"

EXPORT_FUNCTIONS do_configure do_compile do_install

export LDSHARED="${CCLD} -shared"
DEPENDS += "python3-setuptools-native python3-wheel-native"

