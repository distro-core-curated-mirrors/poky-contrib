SUMMARY = "AsyncSSH: Asynchronous SSHv2 client and server library"
DESCRIPTION = "AsyncSSH is a Python package which provides an asynchronous \
client and server implementation of the SSHv2 protocol on top of the Python \
3.6+ asyncio framework."
HOMEPAGE = "http://asyncssh.timeheart.net"
LICENSE = "EPL-2.0 | GPL-2.0-or-later"
LIC_FILES_CHKSUM = "file://COPYRIGHT;md5=a3d68919d4bc3d853512d45cbd1cc345 \
                    file://LICENSE;md5=d9fc0efef5228704e7f5b37f27192723"

SRC_URI[sha256sum] = "e956bf8988d07a06ba3305f6604e261f4ca014c4a232f0873f1c7692fbe3cfc2"

inherit pypi setuptools3 ptest

SRC_URI += " \
    file://run-ptest \
"

PACKAGECONFIG ?= "bcrypt pyopenssl"
PACKAGECONFIG[bcrypt] = ",,,python3-bcrypt"
PACKAGECONFIG[fido2] = ",,,python3-fido2"
PACKAGECONFIG[gssapi] = ",,,python3-gssapi"
PACKAGECONFIG[libnacl] = ",,,python3-libnacl"
PACKAGECONFIG[pkcs11] = ",,,python3-python-pkcs11"
PACKAGECONFIG[pyopenssl] = ",,,python3-pyopenssl"
PACKAGECONFIG[pywin32] = ",,,python3-pywin32"

RDEPENDS:${PN} += "\
    python3-cryptography \
    python3-typing-extensions \
"

RDEPENDS:${PN}-ptest += " \
    python3-pytest \
    python3-unittest-automake-output \
"

do_install_ptest() {
    install -d ${D}${PTEST_PATH}/tests
    cp -rf ${S}/tests/* ${D}${PTEST_PATH}/tests/
}
# WARNING: We were unable to map the following python package/module
# dependencies to the bitbake packages which include them:
#    OpenSSL
#    cryptography.exceptions
#    cryptography.hazmat.backends.openssl
#    cryptography.hazmat.primitives.asymmetric
#    cryptography.hazmat.primitives.asymmetric.padding
#    cryptography.hazmat.primitives.ciphers
#    cryptography.hazmat.primitives.ciphers.aead
#    cryptography.hazmat.primitives.ciphers.algorithms
#    cryptography.hazmat.primitives.ciphers.modes
#    cryptography.hazmat.primitives.hashes
#    cryptography.hazmat.primitives.kdf.pbkdf2
#    cryptography.hazmat.primitives.poly1305
#    cryptography.hazmat.primitives.serialization
#    fido2.ctap
#    fido2.ctap1
#    fido2.ctap2
#    fido2.hid
#    gssapi.exceptions
#    mmapfile
#    pkcs11.util.ec
#    pkcs11.util.rsa
#    sspi
#    sspicon
#    win32api
#    win32con
#    win32ui

RDEPENDS:${PN}:append:class-target = "\
    python3-asyncio \
    python3-core \
    python3-crypt \
    python3-ctypes \
    python3-datetime \
    python3-io \
    python3-math \
    python3-netclient \
    python3-shell \
    python3-stringold \
    python3-unixadmin \
"

