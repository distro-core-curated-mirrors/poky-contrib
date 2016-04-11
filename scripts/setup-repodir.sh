#!/bin/sh

# required args
REPODIR=$1
REPOURL=$2
PWURL=$3
PWPROJECT=$4
PWUSER=$5
PWPASS=$6

usage () {
    echo "usage: $0 <REPODIR> <REPOURL> <PWURL> <PWPROJECT> <PWUSER> <PWPASS>"
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
     -z "$PWPASS" ]; then
    usage
fi

SCRIPTS_DIR=`dirname $0`
PATCHTEST_BASE=`readlink -e $SCRIPTS_DIR/..`
PATCHTEST_GITHOOKS="$PATCHTEST_BASE/hooks"
GITPWDIR=$PATCHTEST_BASE/patchwork/git-pw

cd $PATCHTEST_BASE
. venv/bin/activate && VIRTUALENV=1

PATH="$PATH:$PATCHTEST_BASE:$GITPWDIR"
PYTHONPATH="$PATCHTEST_BASE":"/usr/bin/python:$PYTHONPATH"

# clone the repo if it does not exists
if [ ! -d $REPODIR ]; then
    git clone $REPOURL $REPODIR
fi

# set up the soft links for hooks
REPO_GITHOOKS="$REPODIR/.git/hooks"
[ -e $REPO_GITHOOKS -a ! -e $REPO_GITHOOKS/applypatch-msg ] && { ln -s $PATCHTEST_GITHOOKS/applypatch-msg $REPO_GITHOOKS; }
[ -e $REPO_GITHOOKS -a ! -e $REPO_GITHOOKS/commit-msg ] && { ln -s $PATCHTEST_GITHOOKS/commit-msg $REPO_GITHOOKS; }

# cd into the repository
cd $REPODIR

# pull latest changes the repo
git pull

# set the git pw configuration
[ -n "$PWURL" ] && git config patchwork.default.url $PWURL
[ -n "$PWPROJECT" ] && git config patchwork.default.project $PWPROJECT
[ -n "$PWUSER" ] && git config patchwork.default.user $PWUSER
[ -n "$PWPASSWORD" ] && git config patchwork.default.password $PWPASSWORD

deactivate && unset VIRTUALENV

exit 0

