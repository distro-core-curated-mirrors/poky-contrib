#!/bin/bash

if [ -f /tmp/ps_commEight.txt ]
then
	rm /tmp/ps_comm*
fi

if [ -f /tmp/ps_commOne.txt ]
then
	ps aux | grep [b]itbake > /tmp/ps_commEight.txt
	fileSizeEight=$(cat /tmp/ps_commEight.txt | wc -l)
	fileSizeOne=$(cat /tmp/ps_commOne.txt | wc -l)
	if [ "$fileSizeOne" -lt "$fileSizeEight" ]
	then
		echo passed >> hobResults
	else
		echo failed >> hobResults
	fi
else
	ps aux | grep [b]itbake > /tmp/ps_commOne.txt
fi
