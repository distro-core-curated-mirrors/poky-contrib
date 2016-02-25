#!/bin/sh

REPODIR=$1

SCRIPTS_DIR=`dirname $0`
PATCHTEST_BASE=`readlink -e $SCRIPTS_DIR/..`

cd $REPODIR
git pw poll-events | $PATCHTEST_BASE/patchtest --test-dir $PATCHTEST_BASE/sample-tests/fail --post
exit $@

