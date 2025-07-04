SUMMARY = "A fast Python in-process signal/event dispatching system."
DESCRIPTION = "Blinker provides a fast dispatching system that allows any \
number of interested parties to subscribe to events, or 'signals'."
HOMEPAGE = "https://github.com/pallets-eco/blinker"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE.txt;md5=42cd19c88fc13d1307a4efd64ee90e4e"

SRC_URI[sha256sum] = "b4ce2265a7abece45e7cc896e98dbebe6cead56bcf805a3d23136d145f5445bf"

inherit pypi python_setuptools_build_meta ptest-python-pytest

RDEPENDS:${PN} += "\
        python3-asyncio \
"
