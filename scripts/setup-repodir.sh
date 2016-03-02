#!/bin/sh

#set -x

# required args
REPODIR=$1
REPOURL=$2
PWURL=$3
PWPROJECT=$4
PWUSER=$5
PWPASSWORD=$6

usage () {
    echo "usage: $0 <REPODIR> <REPURL> <PWURL> <PWPROJECT> <PWUSER> <PWPASSWORD>"
    [ -n "$VIRTUALENV" ] && deactivate
    unset VIRTUALENV
    exit 1
}

# check required args
if [ -z "$REPODIR" -o \
     -z "$REPOURL" -o \
     -z "$PWURL" -o \
     -z "$PWPROJECT" -o \
     -z "$PWUSER" -o \
     -z "$PWPASSWORD" ]; then
    usage
fi

SCRIPTS_DIR=`dirname $0`
PATCHTEST_BASE=`readlink -e $SCRIPTS_DIR/..`
GITPWDIR=$PATCHTEST_BASE/patchwork/git-pw

cd $PATCHTEST_BASE
. venv/bin/activate && VIRTUALENV=1

PATH="$PATH:$PATCHTEST_BASE:$GITPWDIR"
PYTHONPATH="$PATCHTEST_BASE":"/usr/bin/python:$PYTHONPATH"

# clone the repo if it does not exists
if [ ! -d $REPODIR ]; then
    git clone $REPOURL $REPODIR
fi

cd $REPODIR
# pull latest changes the repo
git pull

# set the git pw configuration
[ -n "$PWURL" ] && git config patchwork.default.url $PWURL
[ -n "$PWPROJECT" ] && git config patchwork.default.project $PWPROJECT
[ -n "$PWUSER" ] && git config patchwork.default.user $PWUSER
[ -n "$PWPASSWORD" ] && git config patchwork.default.password $PWPASSWORD

# poll all events
while true; do
    events=`git pw poll-events`
    if [ -z "$events" ]; then
	break;
    fi
    echo "Events polled:"
    echo $events
done

deactivate && unset VIRTUALENV

exit 0

