SUMMARY = "cargo applet to build and install C-ABI compatible dynamic and static libraries."
HOMEPAGE = "https://crates.io/crates/cargo-c"
LICENSE = "MIT"
LIC_FILES_CHKSUM = " \
    file://LICENSE;md5=384ed0e2e0b2dac094e51fbf93fdcbe0 \
"

SRC_URI = "crate://crates.io/cargo-c/${PV};name=cargo-c"
SRC_URI[cargo-c.sha256sum] = "fe82742019f0e5c1a9f8549b0f41b20f1bc834f5ed0626c47019f15be566b321"
S = "${CARGO_VENDORING_DIRECTORY}/cargo-c-${PV}"

inherit cargo cargo-update-recipe-crates pkgconfig

DEPENDS = "openssl curl"

require ${BPN}-crates.inc

BBCLASSEXTEND = "native"
