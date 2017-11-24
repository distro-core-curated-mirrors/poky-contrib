#!/bin/sh

# paralell-oe-selftest: executes oe-selftest in 'parallel'. The tests (modules, clases or test methods, same
# as oe-selftest --run-tests) to be executed can be piped to this script; if this is not the case, all modules
# are executed
#
# Copyright (c) 2013-2017 Intel Corporation
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
#

# Before anything else, check oe-core environment
if [ -z "$BUILDDIR" ]; then
    echo "Please initialize the OE-Core environment through oe-init-build-env script"
    exit 1
fi

usage() {
CMD=$(basename $0)
cat <<EOM
Usage: $CMD [-h] [-j jobs] [-- <parallel options>]
  -j jobs             Number of jobs to be running concurrently
  -h                  Display this help message

 Examples:
   # run all tests
   $CMD

   # run just wic and bblayers
   echo wic bblayers | $CMD

EOM
}

JOBS=4
# Parse and validate arguments
while getopts "hj:" OPT; do
	case $OPT in
	j)
	        JOBS="$OPTARG"
	        ;;
	h)
		usage
		exit 0
		;;
	--)
		shift
		break
		;;
	esac
done

shift "$((OPTIND - 1))"
extraopts="$@"

if [ -z "$extraopts" ]; then
    extraopts="--keep-order --progress"
fi

if [ -t 0 ]; then
    # no stdin, run all modules
    TESTCASES="$(oe-selftest -m | awk '{ print $NF } ' | grep -v ':')"
else
    TESTCASES="$(cat /dev/stdin)"
fi

# Parallelization is done through GNU/Paralell, so it must be present in host machine
which parallel 2>&1 >/dev/null || { echo "Please install GNU/Parallel"; exit 1; }

echo "The following tests will be run in parallel with a $JOBS jobs"
echo ""; for t in $TESTCASES; do echo -e "\t$t"; done; echo ""

echo "$TESTCASES" | time parallel --jobs $JOBS $extraopts oe-selftest -r
