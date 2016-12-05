#!/usr/bin/env bash
# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
# test-every-commit: Starting at a certain commit in the past, run patchtest until HEAD
#                    This is useful for scripts requiring pretest execution because
#                    testing patch can be merge in every iteration.
#
# Copyright (C) 2016 Intel Corporation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# defaults values
repo=$1
origin=$2
tests=$3

function usage() {
       echo -e "Runs patchtest starting at certain commit using the specified test suite"
       echo -e "\$ $0 <repo> <since commit> <startdir path of the test suite>"
       echo
       echo -e "For example, test last 10 commits"
       echo
       echo -e "\$ $0 ~/poky HEAD~10 ~/patchtest-oe/tests"
       echo

       exit 1
}

[ -z $repo ]   && { echo "OE-core repo missing"; usage; }
[ -z $origin ] && { echo "Start commit missing"; usage; }
[ -z $tests ]  && { echo "Start directory from a test suite missing"; usage; }

tmpdir=$(mktemp -d)

cd $repo
for commit in $(git rev-list $origin..HEAD --reverse)
do
    patch="$tmpdir/$commit.patch"
    git format-patch "$commit^1..$commit" --stdout > $patch

    CMD="patchtest $patch -r $repo -s $tests --base-commit $commit^1"
    LOG="`$CMD 2>&1`"

    # In case of patchtest failure, just quit showing the patch that breaks it
    if [ $? -ne 0 ]
    then
        echo "patchtest failed with patch $patch"
	echo "Command: $CMD"
	echo "Log: $LOG"
	echo
        break
    else
	echo "Patch $patch"
	echo "Command: $CMD"
	echo "`echo \"$LOG\" | grep FAIL`"
	echo
    fi
done

    
