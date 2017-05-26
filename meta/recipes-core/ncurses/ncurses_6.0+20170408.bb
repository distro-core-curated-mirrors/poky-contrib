require ncurses.inc

SRC_URI += "file://tic-hang.patch \
            file://config.cache \
            file://configure-reproducible.patch \
"
# commit id corresponds to the revision in package version
SRCREV = "9e9f3df43c491e8f046345b9d1aa54ad57201df2"
S = "${WORKDIR}/git"
EXTRA_OECONF += "--with-abi-version=5"
UPSTREAM_CHECK_GITTAGREGEX = "(?P<pver>\d+(\.\d+)+(\+\d+)*)"
