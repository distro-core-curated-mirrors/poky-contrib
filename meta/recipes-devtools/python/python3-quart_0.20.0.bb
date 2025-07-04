SUMMARY = "A Python ASGI web framework with the same API as Flask"
HOMEPAGE = "https://github.com/pallets/quart"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${UNPACKDIR}/LICENSE-quart.txt;md5=a30779ca15b5a14f8a5d6a5462434739"

SRC_URI += "https://raw.githubusercontent.com/pallets/quart/refs/heads/main/LICENSE.txt;name=license-quart;downloadfilename=LICENSE-quart.txt"

SRC_URI[sha256sum] = "08793c206ff832483586f5ae47018c7e40bdd75d886fee3fabbdaa70c2cf505d"
SRC_URI[license-quart.sha256sum] = "70a5a96e77c13378db31e782cbcbac45002f19b674d84c5bacd18b2adb7ae4b4"

inherit pypi python_flit_core

RDEPENDS:${PN} += " \
    python3-aiofiles \
    python3-blinker \
    python3-click \
    python3-flask \
    python3-hypercorn \
    python3-importlib-metadata \
    python3-itsdangerous \
    python3-jinja2 \
    python3-markupsafe \
    python3-typing-extensions \
    python3-werkzeug \
"
