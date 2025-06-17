## This is information on the rust-snapshot (binary) used to build our current release.
## snapshot info is taken from rust/src/stage0
## Rust is self-hosting and bootstraps itself with a pre-built previous version of itself.
## The exact (previous) version that has been used is specified in the source tarball.
## The version is replicated here.

SNAPSHOT_VERSION = "beta"

SRC_URI[rustc-snapshot-aarch64.sha256sum] = "2c4a949aee410d9ed6602c3f95d58895fb0051fe7a3f1d0abd585f3d952a31d7"
SRC_URI[rust-std-snapshot-aarch64.sha256sum] = "88ffb04366bc06c331113026ea64b04ce970f01f13a0e80736fd59676e4e974a"
SRC_URI[cargo-snapshot-aarch64.sha256sum] = "61a8743d62dd505d7d76b2ffd282e2b41653b0b30eb96e7f950f144201270a21"
SRC_URI[clippy-snapshot-aarch64.sha256sum] = "198c679a62e71d108688d3b64a5be76ecd6462f3301c0ee411943678bae640ce"

SRC_URI[rustc-snapshot-i686.sha256sum] = "00506ca8eeca547c844c48165e80afc71fa5bc9ad5734c2b90ebd9d6184540f5"
SRC_URI[rust-std-snapshot-i686.sha256sum] = "b4447663123e42a950943829f661283d6b36f3da14750c811d6704a2edc64b40"
SRC_URI[cargo-snapshot-i686.sha256sum] = "190e8b6bda864b4316f530e5d693e779074de8665a5abe6a4f5cbd01ce8fe6b7"
SRC_URI[clippy-snapshot-i686.sha256sum] = "ef98b85f80e434c49b0c19eca16baab3d10345237642c7252b3ab5ddeb494fba"

SRC_URI[rustc-snapshot-loongarch64.sha256sum] = "09337bbecb0933162c1dcd5c85a5fa430b85c4b541b70f01ba77a82d5e64cbdb"
SRC_URI[rust-std-snapshot-loongarch64.sha256sum] = "7411b776b6fb10d0a10e3de19183caeb9980f523aa014a5b320bb4422f2301a8"
SRC_URI[cargo-snapshot-loongarch64.sha256sum] = "b0789d6fe6d8f7e07f0858211e59ae9278adee7d14dee64fc359b3079773993d"
SRC_URI[clippy-snapshot-loongarch64.sha256sum] = "1eeb173bc287d7fba22091a7083c472aeace48679aae3450c77435376a5285b5"

SRC_URI[rustc-snapshot-powerpc.sha256sum] = "4cc9f12877323f5ebcf7f3d2878800dbc4d0930615b9baeb40e0a2824536d5d9"
SRC_URI[rust-std-snapshot-powerpc.sha256sum] = "4a265f557aca1b2cc3d377be693bf9fe90c4b0ced99e77a406849aaaf3ad7eff"
SRC_URI[cargo-snapshot-powerpc.sha256sum] = "28ab251856c6a252beb72a5db0e18e68e40b342fcbd903dd75811ba393b44194"
SRC_URI[clippy-snapshot-powerpc.sha256sum] = "6b0bcca51760ec121f7ec64e2f6eaf91eeebb9da0318642a115f6852647ae806"

SRC_URI[rustc-snapshot-powerpc64.sha256sum] = "b32b303840f35d6a2f42751cada1f833b4c55b7d83634b1cc6d469902539d168"
SRC_URI[rust-std-snapshot-powerpc64.sha256sum] = "3886265ec1bd94ae47146db67bc2a72fdd9d70b64c74878fc1ef9c50498b9f23"
SRC_URI[cargo-snapshot-powerpc64.sha256sum] = "9a09c0f8d027310b26909c193227466402ef616c27b943ec16cd5a7eabca5ca9"
SRC_URI[clippy-snapshot-powerpc64.sha256sum] = "ccafe9b4403c6bcb87a244eb6afadcbab799e65dc105f60551a8a3b6153c31d9"

SRC_URI[rustc-snapshot-powerpc64le.sha256sum] = "33c763eeedd8f3a3ca885f94ade5c3a2355a479a0186ddae33e4cb068529de72"
SRC_URI[rust-std-snapshot-powerpc64le.sha256sum] = "0c687a9b04b1b36a14c972913dfb9f0d230551f301a895593f1623677b59a26d"
SRC_URI[cargo-snapshot-powerpc64le.sha256sum] = "d187d131e679bebcdae5a7b9e828285f55b61cbc124e72d233725e4e0f2dbc39"
SRC_URI[clippy-snapshot-powerpc64le.sha256sum] = "2db59bb48172923ad3db736f51ccf1226bdb8ebc76daa29e220007897d76bf6d"

SRC_URI[rustc-snapshot-riscv64gc.sha256sum] = "cee9ff6682f8c87d5b81082dd6dd7eea26c59c246ef34c70c934b07a2d520817"
SRC_URI[rust-std-snapshot-riscv64gc.sha256sum] = "f636c9cee16b8e676597b31956d6827e1bac7ccd83c730653953affce9724a96"
SRC_URI[cargo-snapshot-riscv64gc.sha256sum] = "885a2c1e30eb3d489a1234034663131c8762645ec1c03ce94198053a21debfa7"
SRC_URI[clippy-snapshot-riscv64gc.sha256sum] = "0876fae91f3d54a745a73876b901d6551089264b408b7d1954475d3e6195f72b"

SRC_URI[rustc-snapshot-s390x.sha256sum] = "945070094b80ac73cb013d3f556767caf6437258121f76921227e44d18249678"
SRC_URI[rust-std-snapshot-s390x.sha256sum] = "3e164f2c3af1850902a7852d5b043f6ac2065b02d0786912b66c83c1371f71e6"
SRC_URI[cargo-snapshot-s390x.sha256sum] = "bf3d01fc0202bcdea158e22821e1ffb8b07e4324ce487be96cde2cf1f1e5eaf6"
SRC_URI[clippy-snapshot-s390x.sha256sum] = "12d12c1c6a277af5c203ad0fbf6dcb4b04ea74614740734466ea7754f13696f6"

SRC_URI[rustc-snapshot-x86_64.sha256sum] = "14b944631444b666019e0c2f3590b78b3de3dcd499c0f7254dd22a95703e8585"
SRC_URI[rust-std-snapshot-x86_64.sha256sum] = "354c0e9396e7b241a7e8c69e3670d98a42ed8bb7359d4f06deefa4fdf81df675"
SRC_URI[cargo-snapshot-x86_64.sha256sum] = "53921721c33e20275eb7a912ae80af22aa3e888a232360baa3f00f272114833f"
SRC_URI[clippy-snapshot-x86_64.sha256sum] = "52f4b0a2bd2a5d0bdbccfc1a8ad9cf24572c103c8713911e121fde4935c22854"

SRC_URI[rust-std-snapshot-i586.sha256sum] = "2c54755349f8d94511b15b29b527533be186f6865ee1b2022e5345f42b00f5bf"

SRC_URI[rust-std-snapshot-sparc64.sha256sum] = "03d9f75b9a4126c81b1896dcfafadecbbb6f4e81fdc774023f81acc28ed125c9"

SRC_URI += " \
    ${RUST_DIST_SERVER}/dist/2025-05-26/${RUST_STD_SNAPSHOT}.tar.xz;name=rust-std-snapshot-${RUST_BUILD_ARCH};subdir=rust-snapshot-components \
    ${RUST_DIST_SERVER}/dist/2025-05-26/${RUSTC_SNAPSHOT}.tar.xz;name=rustc-snapshot-${RUST_BUILD_ARCH};subdir=rust-snapshot-components \
    ${RUST_DIST_SERVER}/dist/2025-05-26/${CARGO_SNAPSHOT}.tar.xz;name=cargo-snapshot-${RUST_BUILD_ARCH};subdir=rust-snapshot-components \
"

RUST_DIST_SERVER = "https://static.rust-lang.org"

RUST_STD_SNAPSHOT = "rust-std-${SNAPSHOT_VERSION}-${RUST_BUILD_ARCH}-unknown-linux-gnu"
RUSTC_SNAPSHOT = "rustc-${SNAPSHOT_VERSION}-${RUST_BUILD_ARCH}-unknown-linux-gnu"
CARGO_SNAPSHOT = "cargo-${SNAPSHOT_VERSION}-${RUST_BUILD_ARCH}-unknown-linux-gnu"
