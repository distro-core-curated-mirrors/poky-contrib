#!/bin/bash

exit_code () {
	if [ $1 -ne 0 ]
	then
		echo "exit code diffrent than 0"
		echo "wrong $2"
		exit 1
	fi
}



#
# Usage
#

usage () {
cat << EOT
Usage: $ME [-h]
	$ME [-f <file1> <file2]
EOT
}

if [ $# -ne 2 ]
then
	usage
	exit 1
fi

TMP_F1="tmp_f1.csv"
TMP_F2="tmp_f2.csv"


if [ ! -f $1 ]
then
	echo "no $1"
	exit 1
fi


if [ ! -f $2 ]
then
	echo "no $2"
	exit 1
fi

#clean the input files
echo $1
echo $TMP_F1
python clean-csv.py $1 $TMP_F1
exit_code $? $1 

echo $2
echo $TMP_F2
python clean-csv.py $2 $TMP_F2
exit_code $? $2


#diff the files(make sure they contain the same commits)
python diff-csv.py $TMP_F1 $TMP_F2
exit_code $? "diff execution"
