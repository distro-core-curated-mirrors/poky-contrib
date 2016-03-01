#!/bin/sh

REPO=$1

if [ -z $REPO ]; then
    echo "Please call the current script with a path to a repository directory"
    exit 1
fi

if [ ! -d $REPO ]; then
    echo "Repository project does not exist, correct the path"
    exit 1
fi

SCRIPTS_DIR=`dirname $0`

# tools used (git-pw and patchtest)
PATCHTEST_BASE=`readlink -e $SCRIPTS_DIR/..`
GITPWDIR=$PATCHTEST_BASE/patchwork/git-pw

# testdir
TESTDIR=$PATCHTEST_BASE/sample-tests/success

cd $PATCHTEST_BASE
. venv/bin/activate

PATH="$PATH:$PATCHTEST_BASE:$GITPWDIR"
PYTHONPATH="$PATCHTEST_BASE":"/usr/bin/python:$PYTHONPATH"

cd $REPO
git pull
git pw poll-events | \
    patchtest --branch master --post --test-dir $TESTDIR

deactivate

exit 0
