#! /bin/bash

set -e

POKY=$1

# TODO find and export DL_DIR
bitbake buildtools-extended-tarball

BUILDTOOLSDIR=$(mktemp --directory --tmpdir=$BUILDDIR buildtools-XXXX)
# TODO latest one
# TODO native architecture
$BUILDDIR/tmp/deploy/sdk/*-buildtools-extended-nativesdk*.sh -d $BUILDTOOLSDIR -y

. $BUILDTOOLSDIR/environment-setup-*

BUILDDIR=$(mktemp --directory --tmpdir=$POKY build-XXXX)
. $POKY/oe-init-build-env $BUILDDIR
bitbake glibc
