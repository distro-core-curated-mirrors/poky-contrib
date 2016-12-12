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
repo=''
since=''
tests=''
pattern='test*.py'

function usage() {
    cat << EOF
\$ $(basename $0) OPTIONS

where OPTIONS are

    -r <repodir>  : Repository.
    -c <since>    : Starting commit
    -s <startdir> : Test suite start directory
    -p <patern>   : Pattern. Defaults '$pattern'

EOF
>&2

    exit 1
}

while getopts ":r:c:s:p:h" opt; do
    case $opt in
	r)
	    repo=$OPTARG
	    ;;
	c)
	    since=$OPTARG
	    ;;
	s)
	    tests=$OPTARG
	    ;;
	p)
	    pattern="$OPTARG"
	    ;;
	h)
	    usage
	    ;;
	\?)
	    echo "Invalid option: -$OPTARG" >&2
	    usage
	    ;;
	:)
	    echo "Option -$OPTARG requires an argument." >&2
	    usage
	    ;;
    esac
done
shift $((OPTIND-1))


[ -z $repo ]  && { echo "OE-core repo missing"; usage; }
[ -z $since ] && { echo "Start commit missing"; usage; }
[ -z $tests ] && { echo "Start directory from a test suite missing"; usage; }

tmpdir=$(mktemp -d)
tmperror=$(mktemp)

cd $repo
for commit in $(git rev-list $since..HEAD --reverse)
do
    patch="$tmpdir/$commit.patch"
    git format-patch "$commit^1..$commit" --stdout > $patch

    CMD="patchtest $patch -r $repo -s $tests --base-commit $commit^1 --json --pattern $pattern"
    JSON="`$CMD 2>$tmperror`"

    # In case of patchtest failure, just quit showing the patch that breaks it
    if [ $? -ne 0 ]
    then
        echo "patchtest failed with patch $patch"
	echo "Command: $CMD"
	cat $tmperror
	echo
        break
    else
	echo "Command: $CMD"
	echo "$JSON" | create-summary --fail --only-results
	echo
    fi
done

    
