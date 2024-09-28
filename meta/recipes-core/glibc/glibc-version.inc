SRCBRANCH ?= "master"
PV = "2.41+git"
SRCREV_glibc ?= "59b9c2b0ef782e408d63eb0149ba3bd00c5b2065"
SRCREV_localedef ?= "fab74f31b3811df543e24b6de47efdf45b538abc"

GLIBC_GIT_URI ?= "git://sourceware.org/git/glibc.git;protocol=https"

UPSTREAM_CHECK_GITTAGREGEX = "(?P<pver>\d+\.\d+(\.(?!90)\d+)*)"
