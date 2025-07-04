SUMMARY = "A ASGI Server based on Hyper libraries and inspired by Gunicorn"
HOMEPAGE = "https://github.com/pgjones/hypercorn/"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=8b55b0913488ba6e14df06d407f10691"

SRC_URI = "git://github.com/pgjones/hypercorn.git;protocol=https;branch=main"
PV = "0.17.3+git"
SRCREV = "c405deafb22d66587ea0aff4f8fa4f5688b74351"
inherit python_poetry_core ptest-python-pytest


# WARNING: We were unable to map the following python package/module
# runtime dependencies to the bitbake packages which include them:
#    aioquic
#    exceptiongroup python3.11
#    h11
#    h2
#    priority
#    pydata_sphinx_theme
#    python
#    sphinxcontrib_mermaid
#    taskgroup
#    tomli
#    uvloop
#    wsproto


# python3-misc is for wsgiref
RDEPENDS:${PN} = " \
    python3-aioquic \
    python3-h11 \
    python3-h2 \
    python3-misc \
    python3-multiprocessing \
    python3-priority \
    python3-trio \
    python3-typing-extensions \
    python3-wsproto \
"

+RDEPENDS:${PN}-ptest += " \
    python3-pytest-asyncio \
    python3-httpx \
"
