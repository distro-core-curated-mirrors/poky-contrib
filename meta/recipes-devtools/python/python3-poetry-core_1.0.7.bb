SUMMARY = "Poetry PEP 517 Build Backend"
DESCRIPTION = "Poetry PEP 517 Build Backend"
HOMEPAGE = "https://github.com/python-poetry/poetry-core"
BUGTRACKER = "https://github.com/python-poetry/poetry-core"

LICENSE = "Apache-2.0 & BSD-2-Clause & MIT & Unknown"
LIC_FILES_CHKSUM = "file://LICENSE;md5=104d5c3c653aeededf4076773aa4c236 \
                    file://poetry/core/_vendor/attrs.LICENSE;md5=75bb9823a2778b5a2bd9b793fac93ea2 \
                    file://poetry/core/_vendor/jsonschema/COPYING;md5=6554d3a51d7cb0b611891317f3c69057 \
                    file://poetry/core/_vendor/jsonschema/LICENSE;md5=2ecb81765361195731a6f72a89e449fd \
                    file://poetry/core/_vendor/lark-parser.LICENSE;md5=b37b83a9cf129d92ee65aaa71c01ce72 \
                    file://poetry/core/_vendor/packaging/LICENSE;md5=7a6e56c9d54ecd731ab31c52de7942f0 \
                    file://poetry/core/_vendor/packaging/LICENSE.APACHE;md5=29256199be2a609aac596980ffc11996 \
                    file://poetry/core/_vendor/packaging/LICENSE.BSD;md5=f405810d173a1618433827928768bcd2 \
                    file://poetry/core/_vendor/pyparsing.LICENSE;md5=fb46329938e6bc829b256e37d5c1e31a \
                    file://poetry/core/_vendor/pyrsistent/LICENSE.mit;md5=1211a1ac6eac40020d0f99c39b4e4270 \
                    file://poetry/core/_vendor/six.LICENSE;md5=6a574656da93d9ef05431b45907e35b6 \
                    file://poetry/core/_vendor/tomlkit/LICENSE;md5=be329e5ef9c9fe86738c9afe6ef3c11c \
                    file://poetry/core/spdx/license.py;md5=1313b09f1abd30e037225e80908ad108"

SRC_URI[sha256sum] = "98c11c755a16ef6c5673c22ca94a3802a7df4746a0853a70b6fae8b9f5cac206"

inherit pypi setuptools3

# WARNING: the following rdepends are determined through basic analysis of the
# python sources, and might not be 100% accurate.
RDEPENDS:${PN} += "python3-compression python3-core python3-crypt python3-io python3-json python3-logging python3-netclient python3-packaging python3-pathlib2 python3-pprint python3-shell"

# WARNING: We were unable to map the following python package/module
# dependencies to the bitbake packages which include them:
#    jsonschema
#    lark
#    pip._internal.index.collector
#    six.moves.urllib.parse
#    six.moves.urllib.request
#    tomlkit.container
#    tomlkit.exceptions
#    tomlkit.toml_document
#    tomlkit.toml_file
#    urllib2
#    urlparse

BBCLASSEXTEND = "native nativesdk"
