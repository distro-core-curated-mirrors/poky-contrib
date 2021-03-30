#!/bin/sh

flock -w 10 /tmp -c echo; /bin/echo $?
