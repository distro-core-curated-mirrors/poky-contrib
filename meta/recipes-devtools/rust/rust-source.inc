RUST_VERSION ?= "${@d.getVar('PV').split('-')[0]}"

SRC_URI += "https://static.rust-lang.org/dist/rustc-${RUST_VERSION}-src.tar.xz;name=rust \
            file://oeqa-selftest-Increase-timeout-in-process-sigpipe-ru.patch;patchdir=${RUSTSRC} \
            file://revert-link-std-statically-in-rustc_driver-feature.patch;patchdir=${RUSTSRC} \
            file://Zdual-proc-macros-additional-check.patch;patchdir=${RUSTSRC} \
            file://0001-libunwind-Use-gcs-instead-of-gcs-target-attribute.patch;patchdir=${RUSTSRC} \
	    file://rust-oe-selftest.patch;patchdir=${RUSTSRC} \
"
SRC_URI[rust.sha256sum] = "d939eada065dc827a9d4dbb55bd48533ad14c16e7f0a42e70147029c82a7707b"

RUSTSRC = "${WORKDIR}/rustc-${RUST_VERSION}-src"

UPSTREAM_CHECK_URI = "https://forge.rust-lang.org/infra/other-installation-methods.html"
UPSTREAM_CHECK_REGEX = "rustc-(?P<pver>\d+(\.\d+)+)-src"

CVE_STATUS[CVE-2024-24576] = "not-applicable-platform: Issue only applies on Windows"
CVE_STATUS[CVE-2024-43402] = "not-applicable-platform: Issue only applies on Windows"
