#!/bin/sh

REPO=$1

# Poll new events and update timestamp
# Pseudocode:
#
# 1) if timestamp is present and valid, poll new events since $1 and update $1 with last event's timestamp.
#    Function outputs the new events
# 2) if timestamp is not present or invalid, poll ALL events and store the last event's timestamp into $1
#    Function do not output any event

pollevents () {

    # plain text file containing the timestamp of the last series event
    timestamp_filename=$1

    # event filter
    event_filter=$2

    # indicates if the timestamp file was updated or created successfully
    timestamp_updated=""

    # timestamp exists and it has non-zero length, get the timestamp and poll the events
    if [ -e $timestamp_filename ]; then
        timestamp=$(cat $timestamp_filename)
	if [ ! -z $timestamp ]; then
            events=$(git pw poll-events --since $timestamp | grep -i $event_filter)

            # update the timestamp in case there are new events
	    if [ ! -z "$events" ]; then
		echo "$events" | tail -1 | get-timestamp.py > $timestamp_filename
	    fi
	    timestamp_updated="true"
	fi
    fi

    # timestamp does not exist, or invalid
    if [ "x${timestamp_updated}" = "x" ]; then

	# remove previous git-pw timestamp file
	rm -f .git-pw.*.poll.timestamp

        events="";newevents=""

	# poll ALL events
        while true; do
	    events="$newevents"
	    newevents=$(git pw poll-events | grep -i $event_filter)
	    if [ -z "$newevents" ]; then
		break;
	    fi
        done

	# remove git-pw timestamp file create by git-pw poll-events
	rm .git-pw.*.poll.timestamp

	# create timestamp folder(s) if these do not exit
	timestamp_pathname=$(dirname $timestamp_filename)
	if [ ! -d $timestamp_pathname ]; then
	    mkdir -p $timestamp_pathname
	fi

	# if there are no events, create an empty timestamp
	if [ -z "$events" ]; then
	    > $timestamp_filename
	else
            # create the new timestamp
            echo "$events" | tail -1 | get-timestamp.py > $timestamp_filename
	fi

	# Do not take into account previous events
        events=""
    fi

    echo "$events"
}

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
PATCHTEST_SCRIPTS=`readlink -e $SCRIPTS_DIR`
PATCHTEST_BASE=`readlink -e $SCRIPTS_DIR/..`
GITPWDIR=$PATCHTEST_BASE/patchwork/git-pw

cd $PATCHTEST_BASE
. venv/bin/activate

PATH="$PATH:$PATCHTEST_SCRIPTS:$PATCHTEST_BASE:$GITPWDIR"
PYTHONPATH="$PATCHTEST_BASE":"/usr/bin/python:$PYTHONPATH"

cd $REPO

REPO_PATCHTEST="$REPO/.patchtest"
REPO_PATCHTEST_LOCK="$REPO_PATCHTEST/patchtest.lock"
REPO_PATCHTEST_TS="$REPO_PATCHTEST/poll.timestamp"

# there are several types of events in patchwork, but we are just interested in series
PW_SERIES_NEW_REVISION_EVENTS="series-new-revision"

# make sure no patchtest lock exists
if [ ! -e $REPO_PATCHTEST_LOCK ]; then

    # update patchtest and test suites submodules
    git pull; git submodule update --remote

    # poll new series events
    events=$(pollevents $REPO_PATCHTEST_TS $PW_SERIES_NEW_REVISION_EVENTS)

    # execute patchtest
    if [ -n "$events" ]; then
	echo "$events" | patchtest --branch master
    else
	echo "no new events"
    fi
else
    echo "patchtest currently executing, no events polled"
fi

deactivate

exit 0
