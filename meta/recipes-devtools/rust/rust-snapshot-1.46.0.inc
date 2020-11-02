## This is information on the rust-snapshot (binary) used to build our current release.
## snapshot info is taken from rust/src/stage0.txt
## TODO: find a way to add additional SRC_URIs based on the contents of an
##       earlier SRC_URI.
RS_VERSION = "1.45.2"

RUSTC_SNAPSHOT = "rustc-${RS_VERSION}-${BUILD_ARCH}-unknown-linux-gnu"
RUST_STD_SNAPSHOT = "rust-std-${RS_VERSION}-${BUILD_ARCH}-unknown-linux-gnu"
CARGO_VERSION = "0.46.1"
CARGO_SNAPSHOT = "cargo-${CARGO_VERSION}-${BUILD_ARCH}-unknown-linux-gnu"

SRC_URI += " \
	https://static.rust-lang.org/dist/${RUSTC_SNAPSHOT}.tar.xz;name=rustc-snapshot-${BUILD_ARCH};subdir=rust-snapshot-components \
	https://static.rust-lang.org/dist/${RUST_STD_SNAPSHOT}.tar.xz;name=rust-std-snapshot-${BUILD_ARCH};subdir=rust-snapshot-components \
	https://static.rust-lang.org/dist/${CARGO_SNAPSHOT}.tar.xz;name=cargo-snapshot-${BUILD_ARCH};subdir=rust-snapshot-components \
	"

# TODO: Add hashes for other architecture toolchains as well. Make a script?
SRC_URI[rust-std-snapshot-aarch64.sha256sum] = "d0006b1ec413cd0f698195584cc478d3ceb44ea4232fe1971970be22f1470e1d"
SRC_URI[rust-std-snapshot-x86_64.sha256sum] = "02309322467af8e37256ccf1f064f5233c7fca4423dffde0bd5eb32cde46942a"
SRC_URI[rustc-snapshot-aarch64.sha256sum] = "efcdb593c79a5ecf7a5a62297de92137290299d1ef9fb25129b5cdc81879c01e"
SRC_URI[rustc-snapshot-x86_64.sha256sum] = "0be5c8506fd9317c7d0dc8044b5fef8501caa74f88a9a22be795d68362dc57f6"
SRC_URI[cargo-snapshot-aarch64.sha256sum] = "caccf4f85703c6de77f143e7e24cc5e40a02f23e3d1138aa965922b4531023b6"
SRC_URI[cargo-snapshot-x86_64.sha256sum] = "a27eb5d47b520ef2c554605bf789f80652af63531b4f6a1195d61b3dfd0f6e9c"
