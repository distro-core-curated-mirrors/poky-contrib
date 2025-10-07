## This is information on the rust-snapshot (binary) used to build our current release.
## snapshot info is taken from rust/src/stage0
## Rust is self-hosting and bootstraps itself with a pre-built previous version of itself.
## The exact (previous) version that has been used is specified in the source tarball.
## The version is replicated here.

SNAPSHOT_VERSION = "beta"
COMPILER_DATE = "2025-09-21"

SRC_URI[rustc-snapshot-aarch64.sha256sum] = "3a2bed859214bbea2cdd13675eaf480e62c01646efed26067ba7078e6dd8591f"
SRC_URI[rust-std-snapshot-aarch64.sha256sum] = "89a808aade0a91043bef23f3e3f38d193b4f02b6556f01cbaf103c43ce428478"
SRC_URI[cargo-snapshot-aarch64.sha256sum] = "e9f4c66995b8e955e86a67c44fd8d7f6e7349645393bfa605c6c1bb0afc7b930"
SRC_URI[clippy-snapshot-aarch64.sha256sum] = "0c278a9aaa1ae41bd9bd96f52fed50b1a11a65822024fd01a9eacfa3aa8f1de9"

SRC_URI[rustc-snapshot-i686.sha256sum] = "c98df2f0156c3065179f50d55dafda8c5db1f2eae99ecb3f568a8861299be289"
SRC_URI[rust-std-snapshot-i686.sha256sum] = "bc95dd6129e90c9275e0340962993de7a0842040bdfcde9aa419f227d79dbf31"
SRC_URI[cargo-snapshot-i686.sha256sum] = "1fe31a0e463736a9ae90ef11c1e3c7b7972eb82779ecdf5b6bff1f643684a014"
SRC_URI[clippy-snapshot-i686.sha256sum] = "22b9b2b27d0b6b1fd88d67b18d34a4a91207e6b64ba8d47dbfd0c58763d429b3"

SRC_URI[rustc-snapshot-loongarch64.sha256sum] = "c906f519bc65a3a7514a62f8920d334bc10623a76dd2d3464af88065b79cb334"
SRC_URI[rust-std-snapshot-loongarch64.sha256sum] = "5b578548a62dfd3902920719acd17550f45d0e9106049cbdc1f36c8907a8291f"
SRC_URI[cargo-snapshot-loongarch64.sha256sum] = "222010f8428a3d165801d95a820b639ac930747af3cb4a42a25548330585f73e"
SRC_URI[clippy-snapshot-loongarch64.sha256sum] = "afd8c55fa82482a852b564511c4fdddf12abbffc0bbee1b0b4155fd1d6c04105"

SRC_URI[rustc-snapshot-powerpc.sha256sum] = "40f3a5fc7478b40153ab20e3f14a6d838c80dda529481735e898de989a31f963"
SRC_URI[rust-std-snapshot-powerpc.sha256sum] = "4abcda8b23d17f6e6681329b54215f37cca5fc1f3383e58dd60c38220f5528de"
SRC_URI[cargo-snapshot-powerpc.sha256sum] = "db5c4ce1a1a4d87cca4fb64a6c533cc5ab1c94e25e69b26e13808b0fa5e853e9"
SRC_URI[clippy-snapshot-powerpc.sha256sum] = "93333f47a041d4ddea4fd9ad3fb3ab43c40fcee4fabe6405190fa26d6bfe3e2a"

SRC_URI[rustc-snapshot-powerpc64.sha256sum] = "b9efeb2e185e43775d309d083d8c4f45e30e18b7af71b9c45e397af6bc723fcf"
SRC_URI[rust-std-snapshot-powerpc64.sha256sum] = "7579f587df01fb55211e6a0a61ed96f14955b7f56990e679715157b06b49fe79"
SRC_URI[cargo-snapshot-powerpc64.sha256sum] = "8878cf473faf120efb80bac0564b193f3baa14a9027fb4c060574e6fc921edcc"
SRC_URI[clippy-snapshot-powerpc64.sha256sum] = "fb3d68e09e40cbf7d6c330c3866c37c759ed728c1d8cbeb6e8e834f6a1fce1c9"

SRC_URI[rustc-snapshot-powerpc64le.sha256sum] = "8576ae6d787b0f8b127bb2dbeee213cc6093ba92dc7d5ff08f463d56e2e6ce90"
SRC_URI[rust-std-snapshot-powerpc64le.sha256sum] = "d612ed01011c1e7f24b08318029523f6b7ffb12ec38b1f41ebcedf463f924430"
SRC_URI[cargo-snapshot-powerpc64le.sha256sum] = "92734c444e0156e16c8d8998a8432b24d9d01b82da15123508d0002eb008b9bb"
SRC_URI[clippy-snapshot-powerpc64le.sha256sum] = "d6705b1e6722e3faf5b863fb319cd811fcb27f4a564e633f164f02f8699c9255"

SRC_URI[rustc-snapshot-riscv64gc.sha256sum] = "db5a862a260fe8688e3b1da1161948eed5361723a296bb27dcc62758eaa2b873"
SRC_URI[rust-std-snapshot-riscv64gc.sha256sum] = "395f2975bc86a63736ba7661985db038efa5f5982459add18201c97e4b1a9200"
SRC_URI[cargo-snapshot-riscv64gc.sha256sum] = "3be5932af030c758a84bc09cbb1c2bc5abecc4e7d8a82de58c2a069ad36e737e"
SRC_URI[clippy-snapshot-riscv64gc.sha256sum] = "2ed67a738a07e9d07c1db7789cc5ebe7af033334670fcb1ce84441b9e474ec0c"

SRC_URI[rustc-snapshot-s390x.sha256sum] = "69eedf71d20924d9729684e27a3a8cebc60efa7c0e7a3f8b6fe664f469a36788"
SRC_URI[rust-std-snapshot-s390x.sha256sum] = "8f149e17d654de210a71ace9db03f23bd1a80d0e2c17f8336da2b1ec2315c8a0"
SRC_URI[cargo-snapshot-s390x.sha256sum] = "3d163f9fdc2b8b0f5cbbf846caf1dccaee07984d8783250e8988ef447e53663d"
SRC_URI[clippy-snapshot-s390x.sha256sum] = "78231b81d8e612a4c41828428ba2e9af926f2119308b291c8ce81a5233c3c6a6"

SRC_URI[rustc-snapshot-x86_64.sha256sum] = "5d3c1fceba5285bc54f5a327841ecb8893e719ba874e483c904b903f4dc293ed"
SRC_URI[rust-std-snapshot-x86_64.sha256sum] = "b60da22feb82c21128a151013c690cdef1c291de33e1b6ada5dcc95d3bff3899"
SRC_URI[cargo-snapshot-x86_64.sha256sum] = "07aa13a5411a49238b31191a0797d63b74120a1fa9b5658a67f6c1065271c30c"
SRC_URI[clippy-snapshot-x86_64.sha256sum] = "217255d6ea157f7b06aa66d033dca6239bbc296bc14ff3f0017d5c68bb4d1022"

SRC_URI[rust-std-snapshot-i586.sha256sum] = "665d5a0debd829f3682572e4c3578d41bec58b01df10cc8c71ca66d326a3579f"

SRC_URI[rust-std-snapshot-sparc64.sha256sum] = "92af1bc3beaf80a763aac682a15957d82771fc619d446fb4327f4e8be229438d"

SRC_URI += " \
    ${RUST_DIST_SERVER}/dist/${COMPILER_DATE}/${RUST_STD_SNAPSHOT}.tar.xz;name=rust-std-snapshot-${RUST_BUILD_ARCH};subdir=rust-snapshot-components \
    ${RUST_DIST_SERVER}/dist/${COMPILER_DATE}/${RUSTC_SNAPSHOT}.tar.xz;name=rustc-snapshot-${RUST_BUILD_ARCH};subdir=rust-snapshot-components \
    ${RUST_DIST_SERVER}/dist/${COMPILER_DATE}/${CARGO_SNAPSHOT}.tar.xz;name=cargo-snapshot-${RUST_BUILD_ARCH};subdir=rust-snapshot-components \
"

RUST_DIST_SERVER = "https://static.rust-lang.org"

RUST_STD_SNAPSHOT = "rust-std-${SNAPSHOT_VERSION}-${RUST_BUILD_ARCH}-unknown-linux-gnu"
RUSTC_SNAPSHOT = "rustc-${SNAPSHOT_VERSION}-${RUST_BUILD_ARCH}-unknown-linux-gnu"
CARGO_SNAPSHOT = "cargo-${SNAPSHOT_VERSION}-${RUST_BUILD_ARCH}-unknown-linux-gnu"
