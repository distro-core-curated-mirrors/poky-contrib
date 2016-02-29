#!/bin/sh

set -x

SCRIPTS_DIR=`dirname $0`
PATCHTEST_BASE=`readlink -e $SCRIPTS_DIR/..`
REQUIREMENTS_FILENAME='requirements.txt'
VENV_NAME="venv"

# fetch all submodules
git submodule update --remote

# install all python requirements
cd $PATCHTEST_BASE

virtualenv $VENV_NAME

. $VENV_NAME/bin/activate

REQUIREMENTS_FILES=$(find $PATCHTEST_BASE -name $REQUIREMENTS_FILENAME)

for req in $REQUIREMENTS_FILES; do
    pip install -r $req
done

deactivate

exit 0
