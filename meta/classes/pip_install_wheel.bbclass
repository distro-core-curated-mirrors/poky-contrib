DEPENDS:append = " python3-pip-native"

# The directory where wheels should be written too
PIP_INSTALL_DIST_PATH ?= "${WORKDIR}/dist"

PIP_INSTALL_ARGS ?= "\
    -vvvv \
    --ignore-installed \
    --no-cache \
    --no-deps \
    --no-index \
    --root=${D} \
    --prefix=${prefix} \
"

PIP_INSTALL_PYTHON = "python3"
PIP_INSTALL_PYTHON:class-native = "nativepython3"

pip_install_wheel_do_install () {
    test -f ${PIP_INSTALL_DIST_PATH}/*.whl || bbfatal No wheels generated in ${PIP_INSTALL_DIST_PATH}

    nativepython3 -m pip install ${PIP_INSTALL_ARGS} ${WHEEL_DIST_DIR}/*.whl ||
      bbfatal_log "Failed to pip install wheel. Check the logs."

    cd ${D}
    for i in ${D}${bindir}/* ${D}${sbindir}/*; do
        if [ -f "$i" ]; then
            sed -i -e "1s,#!.*nativepython3,#!${USRBINPATH}/env ${PIP_INSTALL_PYTHON}," $i
            sed -i -e "s:${PYTHON}:${USRBINPATH}/env\ ${PIP_INSTALL_PYTHON}:g" $i
            sed -i -e "s:${STAGING_BINDIR_NATIVE}:${bindir}:g" $i
            nativepython3 -mpy_compile $(realpath --relative-to=${D} $i)
        fi
    done
}

EXPORT_FUNCTIONS do_install
