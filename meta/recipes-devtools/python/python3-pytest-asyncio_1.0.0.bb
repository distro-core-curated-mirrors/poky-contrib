DESCRIPTION = "pytest-asyncio is an Apache2 licensed library, written in Python, for testing asyncio code with pytest"

LICENSE = "Apache-2.0"
LIC_FILES_CHKSUM = "file://LICENSE;md5=136e4f49dbf29942c572a3a8f6e88a77"

SRC_URI[sha256sum] = "d15463d13f4456e1ead2594520216b225a16f781e144f8fdf6c5bb4667c48b3f"

inherit pypi python_setuptools_build_meta ptest-python-pytest

PYPI_PACKAGE = "pytest_asyncio"

DEPENDS += "python3-setuptools-scm-native"

RDEPENDS:${PN} += " \
    python3-pytest \
"

RDEPENDS:${PN}-ptest += " \
    python3-hypothesis \
"

do_install_ptest:append() {
    rm ${D}/${PTEST_PATH}/tests/async_fixtures/test_async_fixtures.py
}

BBCLASSEXTEND = "native nativesdk"
