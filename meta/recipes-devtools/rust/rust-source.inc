RUST_VERSION ?= "${@d.getVar('PV').split('-')[0]}"

SRC_URI += "https://static.rust-lang.org/dist/2025-06-16/rustc-nightly-src.tar.xz;name=rust \
	    file://disable-rustfmt-check.patch;patchdir=${RUSTSRC} \
"
SRC_URI[rust.sha256sum] = "d83737fcf46835deda054fcc0086d84fab924276702befc000f4d0e59b4efc43"

RUSTSRC = "${WORKDIR}/rustc-nightly-src"

UPSTREAM_CHECK_URI = "https://forge.rust-lang.org/infra/other-installation-methods.html"
UPSTREAM_CHECK_REGEX = "rustc-(?P<pver>\d+(\.\d+)+)-src"

CVE_STATUS[CVE-2024-24576] = "not-applicable-platform: Issue only applies on Windows"
CVE_STATUS[CVE-2024-43402] = "not-applicable-platform: Issue only applies on Windows"
