require python-pycryptodome.inc
inherit python_setuptools_build_meta

SRC_URI[sha256sum] = "09609209ed7de61c2b560cc5c8c4fbf892f8b15b1faf7e4cbffac97db1fffda7"

inherit ptest-pydeps
PTEST_PYDEPS_MODULES = "Crypto.Cipher Crypto.Hash Crypto.Protocol Crypto.PublicKey Crypto.Util Crypto.Signature Crypto.IO Crypto.Math"
