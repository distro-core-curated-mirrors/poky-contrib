#!/bin/sh

TIMEOUT=$1
DIRECTORY=$2

flock -w $TIMEOUT $DIRECTORY -c echo; /bin/echo $?
