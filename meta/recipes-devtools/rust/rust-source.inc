RUST_VERSION ?= "${@d.getVar('PV').split('-')[0]}"

SRC_URI += "https://static.rust-lang.org/dist/2025-10-05/rustc-nightly-src.tar.xz;name=rust \
            file://0001-Define-more-ioctl-codes-on-riscv32gc-unknown-linux-g.patch;patchdir=${RUSTSRC} \
            file://rust-oe-selftest.patch;patchdir=${RUSTSRC} \
            file://oeqa-selftest-Increase-timeout-in-process-sigpipe-ru.patch;patchdir=${RUSTSRC} \
            file://0001-src-core-build_steps-tool.rs-switch-off-lto-for-rust.patch;patchdir=${RUSTSRC} \
            file://revert-link-std-statically-in-rustc_driver-feature.patch;patchdir=${RUSTSRC} \
            file://disable-rustfmt-check.patch;patchdir=${RUSTSRC} \
"
SRC_URI[rust.sha256sum] = "09c8cfada4cc71107c2f9712918c75dcd0ec6048bf58b638e18c3fb6196452e7"

RUSTSRC = "${UNPACKDIR}/rustc-nightly-src"

UPSTREAM_CHECK_URI = "https://forge.rust-lang.org/infra/other-installation-methods.html"
UPSTREAM_CHECK_REGEX = "rustc-(?P<pver>\d+(\.\d+)+)-src"
