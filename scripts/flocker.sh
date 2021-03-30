#!/bin/sh

TIMEOUT=$1
DIRECTORY=$2

echo $DIRECTORY

flock -w $TIMEOUT $DIRECTORY -c echo; /bin/echo $?
