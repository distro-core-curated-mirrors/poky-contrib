#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

inherit setuptools3-base python_pep517

DEPENDS += "python3-setuptools-native python3-wheel-native"

SETUPTOOLS_BUILD_ARGS ?= ""

SETUPTOOLS_SETUP_PATH ?= "${S}"

setuptools3_do_configure() {
    :
}

SETUPTOOLS_SKIP_BUILD_BACKEND_CHECK ?= "0"

python check_for_pyprojecttoml_build_backend() {
    import os
    try:
        import tomllib
    except ModuleNotFoundError:
        bb.debug(3, 'tomllib not found, falling back to tomli')
        try:
            import tomli as tomllib
        except ImportError:
            bb.warn('Need either tomli or tomllib in the host environment')
            return
    from pathlib import Path

    if d.getVar('SETUPTOOLS_SKIP_BUILD_BACKEND_CHECK') == "1":
        bb.debug(3, "Skipping check for build-backend in pyproject.toml")
        return 0
    warn_string = "The source has a pyproject.toml which declares '%s' as a build backend, please consider 'inherit %s' instead of inheriting setuptools3."
    warn_layer_string = "The source has a pyproject.toml which declares '%s' as a build backend, please consider 'inherit %s' from %s instead of inheriting setuptools3."
    pyprojecttoml_file = Path(d.getVar('S'), 'pyproject.toml')
    if pyprojecttoml_file.exists():
        bb.debug(3, "pyproject.toml found: %s" % pyprojecttoml_file)
        with open(pyprojecttoml_file, "rb") as f:
            pyprojecttoml_dict = tomllib.load(f)
            try:
                build_system = pyprojecttoml_dict["build-system"]
                if build_system:
                    bb.debug(3, "[build-system] found in pyproject.toml")
                    backend = build_system.get('build-backend')
                    if backend:
                        bb.debug(3, "build-backend found: %s" % backend)
                    if backend == "flit_core.buildapi":
                        bb.warn(warn_string % ('flit_core.buildapi',
                                               'python_flit_core'))
                    elif backend == "setuptools.build_meta":
                        bb.warn(warn_string % ('setuptools.build_meta',
                                              'python_setuptools_build_meta'))
                    elif backend == "poetry.core.masonry.api":
                        bb.warn(warn_layer_string % ('poetry.core.masonry.api',
                                                     'python_poetry_core'))
                    elif backend == "hatchling.build":
                        bb.warn(warn_layer_string % ('hatchling.build',
                                                     'python_hatchling'))
                    elif backend == "maturin":
                        bb.warn(warn_layer_string % ('maturin',
                                                     'python_maturin'))
                    else:
                        bb.warn("The source has a pyproject.toml which declares '%s' as a build backend, but this is not currently supported in oe-core." % backend)
            except KeyError:
                bb.warn("The source has a pyproject.toml, but either no [build-system] or it is malformed. If the recipe is still buildable with setuptools3, you can skip this check with:\nSETUPTOOLS_SKIP_BUILD_BACKEND_CHECK= \"1\"")
                pass
}
do_configure[prefuncs] += "check_for_pyprojecttoml_build_backend"

setuptools3_do_compile() {
        cd ${SETUPTOOLS_SETUP_PATH}
        NO_FETCH_BUILD=1 \
        STAGING_INCDIR=${STAGING_INCDIR} \
        STAGING_LIBDIR=${STAGING_LIBDIR} \
        ${STAGING_BINDIR_NATIVE}/python3-native/python3 setup.py \
        bdist_wheel --verbose --dist-dir ${PEP517_WHEEL_PATH} ${SETUPTOOLS_BUILD_ARGS} || \
        bbfatal_log "'python3 setup.py bdist_wheel ${SETUPTOOLS_BUILD_ARGS}' execution failed."
}
setuptools3_do_compile[vardepsexclude] = "MACHINE"
do_compile[cleandirs] += "${PEP517_WHEEL_PATH}"

# This could be removed in the future but some recipes in meta-oe still use it
setuptools3_do_install() {
        python_pep517_do_install
}

EXPORT_FUNCTIONS do_configure do_compile do_install

export LDSHARED="${CCLD} -shared"
