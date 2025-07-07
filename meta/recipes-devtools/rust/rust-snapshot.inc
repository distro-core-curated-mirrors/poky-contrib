## This is information on the rust-snapshot (binary) used to build our current release.
## snapshot info is taken from rust/src/stage0
## Rust is self-hosting and bootstraps itself with a pre-built previous version of itself.
## The exact (previous) version that has been used is specified in the source tarball.
## The version is replicated here.

SNAPSHOT_VERSION = "beta"

SRC_URI[rustc-snapshot-aarch64.sha256sum] = "3d37128f78af2b6fffb661dc05c2f7ace3a8307b3d60176fcc2b70bd4d802b90"
SRC_URI[rust-std-snapshot-aarch64.sha256sum] = "010bae09b5a25a7b1b0c1a10dc67f5d7db89212fa9ef7149cea4e4f586d5f252"
SRC_URI[cargo-snapshot-aarch64.sha256sum] = "cf7ec78f834f41c658179524a741b472c7ab4bbed3d6c0d7f61e7147d7353a78"
SRC_URI[clippy-snapshot-aarch64.sha256sum] = "3325ddf5704811e48b1f50daea60961d18296ac1626e68828c9eb757e52cf65a"

SRC_URI[rustc-snapshot-i686.sha256sum] = "8791d2c9321b36d64280902e0ec04b85728715bdd072f859fbe3d533209504de"
SRC_URI[rust-std-snapshot-i686.sha256sum] = "d7c351e3a45181f040acd5f8c20c655d878a0d53927489891603b91c80c4abb6"
SRC_URI[cargo-snapshot-i686.sha256sum] = "c0c5c0f72726b577fec05670b6f9d46501b79af55c642d2b2f58a88e731db7ea"
SRC_URI[clippy-snapshot-i686.sha256sum] = "b84d9b6918e18540e3073d66e9bc02845257fe2f1a39c9e62b44e81f2aae341d"

SRC_URI[rustc-snapshot-loongarch64.sha256sum] = "a2a109408ba5db4540ad7bbd1e67a9623aae96203c0238aca5fb3c3741ead97f"
SRC_URI[rust-std-snapshot-loongarch64.sha256sum] = "5418975da12a39cecfb1a040dbb2ae6b8b63a76b652aca582ce04aeebb3c05fb"
SRC_URI[cargo-snapshot-loongarch64.sha256sum] = "7f8dc8897f88659268ed0247bce6fd35b4de813fcac5bd488d20c28504bee028"
SRC_URI[clippy-snapshot-loongarch64.sha256sum] = "332e8549d7bedf4f97dd9b1cb8a5af47fc56374438e8878ebad2593bd36a48b6"

SRC_URI[rustc-snapshot-powerpc.sha256sum] = "7785929842939af15a8404f666c95e5786ca0941f1c15dc084f26a5124411e2c"
SRC_URI[rust-std-snapshot-powerpc.sha256sum] = "96bb329f992b3c8e060796e52aca2ba384225f350ccc2c12d0aa8022b1305842"
SRC_URI[cargo-snapshot-powerpc.sha256sum] = "c81c32af1c4e7e432112515af1dbdd6e4adbea668710881b63af7acd5c4715f9"
SRC_URI[clippy-snapshot-powerpc.sha256sum] = "b4f5e016c5035cd2b70d4e3fbdf1d0ebcd0d1cc6f1d297bc04f99581a02febc5"

SRC_URI[rustc-snapshot-powerpc64.sha256sum] = "3cd480374907eb3816c8db73973abc676c96bc9598943dc89056eb5542d6b6b8"
SRC_URI[rust-std-snapshot-powerpc64.sha256sum] = "e4bcfd4ffb2db92ff57f881875755b9808744c8e59efb2a3ae9c215a05e696ea"
SRC_URI[cargo-snapshot-powerpc64.sha256sum] = "55cd74747e6993eee6ec3aba36a79d108bf952d64a646696883e33798b27ade7"
SRC_URI[clippy-snapshot-powerpc64.sha256sum] = "0dbcfc800635438f803888caaf37677b424ef5a90cab81ceaac627bba7faf6b5"

SRC_URI[rustc-snapshot-powerpc64le.sha256sum] = "c670f5201c14464d9e13da1922609369e784a1e482162cf3e9ed281fce926b01"
SRC_URI[rust-std-snapshot-powerpc64le.sha256sum] = "d05626a5f3c364aba66aa214530fbf37a38b7c613c8c1a54c5ba46d66477db96"
SRC_URI[cargo-snapshot-powerpc64le.sha256sum] = "7fe952473dca82b599745a9f3578b4976e43a6f91bba02a59da216a748d3a3f7"
SRC_URI[clippy-snapshot-powerpc64le.sha256sum] = "7a56be9e5d58dbd2531d8c049fada5bdff5d98436afb63b92ddfc5f58d5835f9"

SRC_URI[rustc-snapshot-riscv64gc.sha256sum] = "1c2b2090ab6ec51df85e6495389adceca4fd414a709d2219fd7b39d1c47c7a49"
SRC_URI[rust-std-snapshot-riscv64gc.sha256sum] = "b43a87dbd6ab3b3d440f2bbeeacc77719d29347b980e74160301539902f039ea"
SRC_URI[cargo-snapshot-riscv64gc.sha256sum] = "f963720adb03fdc4508d7037937345109973e1b15f9590ba7393dac26c493b6b"
SRC_URI[clippy-snapshot-riscv64gc.sha256sum] = "dcfa6d2fcfb96aed0ce6df6bf53cb8cdfe8529fb361cfaa78b92fc8773cc7446"

SRC_URI[rustc-snapshot-s390x.sha256sum] = "742c09735a0b50acea601dfd2ae41e931cbb44d7700d6cba18df9e0ccb45bad8"
SRC_URI[rust-std-snapshot-s390x.sha256sum] = "2bb94be7f6ee32bc23748e69e399a5fd087671e3e4fd8d77e819e51dff8cee5c"
SRC_URI[cargo-snapshot-s390x.sha256sum] = "a214a89077adacb0e73acf6c7b0a312822eb72313be88aa5a1865dee7fba8dbe"
SRC_URI[clippy-snapshot-s390x.sha256sum] = "46db14272bd41ec2b89d146f8d200cf21b12bdb1183fbc303f8e8cebdf11080e"

SRC_URI[rustc-snapshot-x86_64.sha256sum] = "4fdc2e7a65b3924d1577229fe02975a4618481aac35053426abd2b9ede18afde"
SRC_URI[rust-std-snapshot-x86_64.sha256sum] = "c71ecb0a0c44cb7a9f35b6fe71e73f605d025af16f1ee5f1fd9c8a432144c54a"
SRC_URI[cargo-snapshot-x86_64.sha256sum] = "93eeaf15597a264f552c6d60d3d833f15503f6dcc7d909f4138e1daedd56bdd9"
SRC_URI[clippy-snapshot-x86_64.sha256sum] = "c3b96035b40c01c23256ad5b4c2ba876e84e8bc5cfdc6c14cfc9d4eaf57fd74b"

SRC_URI[rust-std-snapshot-i586.sha256sum] = "5ca691898ea3cc66822aa32ac9d24996610cd79e34275b35a53e252f5c99fae7"

SRC_URI[rust-std-snapshot-sparc64.sha256sum] = "84179facb34fb286545622407ac6bfd5bb2b7546e02e56597152ab5bab49fe93"

SRC_URI += " \
    ${RUST_DIST_SERVER}/dist/2025-06-24/${RUST_STD_SNAPSHOT}.tar.xz;name=rust-std-snapshot-${RUST_BUILD_ARCH};subdir=rust-snapshot-components \
    ${RUST_DIST_SERVER}/dist/2025-06-24/${RUSTC_SNAPSHOT}.tar.xz;name=rustc-snapshot-${RUST_BUILD_ARCH};subdir=rust-snapshot-components \
    ${RUST_DIST_SERVER}/dist/2025-06-24/${CARGO_SNAPSHOT}.tar.xz;name=cargo-snapshot-${RUST_BUILD_ARCH};subdir=rust-snapshot-components \
"

RUST_DIST_SERVER = "https://static.rust-lang.org"

RUST_STD_SNAPSHOT = "rust-std-${SNAPSHOT_VERSION}-${RUST_BUILD_ARCH}-unknown-linux-gnu"
RUSTC_SNAPSHOT = "rustc-${SNAPSHOT_VERSION}-${RUST_BUILD_ARCH}-unknown-linux-gnu"
CARGO_SNAPSHOT = "cargo-${SNAPSHOT_VERSION}-${RUST_BUILD_ARCH}-unknown-linux-gnu"
