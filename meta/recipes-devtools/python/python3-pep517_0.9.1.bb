SUMMARY = "Wrappers to build Python packages using PEP 517 hooks"
HOMEPAGE = "https://github.com/pypa/pep517"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://LICENSE;md5=aad69c93f605003e3342b174d9b0708c \
                    file://tests/samples/pkg2/pkg2-0.5.dist-info/LICENSE;md5=aad69c93f605003e3342b174d9b0708c \
                    file://tests/samples/pkg1/pkg1-0.5.dist-info/LICENSE;md5=aad69c93f605003e3342b174d9b0708c"

SRC_URI[sha256sum] = "aeb78601f2d1aa461960b43add204cc7955667687fbcf9cdb5170f00556f117f"
SRC_URI[sha384sum] = "6dc5809f97d4c15e7fef079bb56f5731312549302a96c4541f5ea5a874059e14f2c1f51f7016acf74c27a787e582792c"
SRC_URI[sha512sum] = "7c7d181d52a6d042ad432c4366021f9b2364c77193d99066668acd4c6967dab299644febf0dc4a6efb9a777a0aaae7df2687191cba3f3b93e6bf06ee0769a7df"

S = "${WORKDIR}/pep517-${PV}"

inherit pypi distutils3

RDEPENDS_${PN} += " \
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
#    zipp

BBCLASSEXTEND = "native nativesdk"
