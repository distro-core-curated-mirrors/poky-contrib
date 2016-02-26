#!/bin/sh

# For the moment, all is hardcoded
POKYDIR=$HOME/poky
GITPWDIR=$HOME/patchwork/git-pw

SCRIPTS_DIR=`dirname $0`
PATCHTEST_BASE=`/bin/readlink -e $SCRIPTS_DIR/..`
TESTDIR=$PATCHTEST_BASE/sample-tests/success

cd $PATCHTEST_BASE
. venv/bin/activate

PATH="$PATH:$PATCHTEST_BASE:$GITPWDIR"
PYTHONPATH="$PATCHTEST_BASE":"/usr/bin/python:$PYTHONPATH"

cd $POKYDIR;git pw poll-events | patchtest -d

deactivate

exit 0
