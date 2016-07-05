#!/bin/bash

origin=$1
test_suite=$2

usage() {
    echo -e "Runs patchtest starting at certain commit using the specified test suite"
    echo -e "\$ $0 <since commit> <path to test suite>"
    echo
    echo -e "For example, test last 10 commits"
    echo
    echo -e "\$ $0 HEAD~10 $HOME/patchtest-oe/tests"
    echo
}

[ -z $origin ] || { usage; exit -1; }
[ -z $test_suite ] || { usage; exit -1; }

tmp=$(mktemp)

for commit in $(git rev-list $origin..HEAD --reverse); do
    git format-patch "$commit^1..$commit" --stdout > $tmp
    patchtest --commit "$commit^1" -m $tmp --test-dir $test_suite
done

rm $tmp
