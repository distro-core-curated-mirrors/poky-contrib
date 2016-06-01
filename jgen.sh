#!/bin/bash
ME=$(basename $0)
#INPUT_FILE=input.csv

# Usage

usage () {
cat << EOT
Usage: 	$ME [-h]
	$ME [-v <value>] [-f <file1> <file2>]
	
Options: 
	-h
		Display help.
	-f <file1> <file2>
		Use <file> as input file. The <file> must be in *.csv format.
	-v <value>
		Value for type of build. Value reference:
			 3 - bitbakecore-image-sato
			 4 - bitbake virtual/kernel
			 5 - bitbake core-image-sato (rm_work)
			 6 - bitbake core-image-sato -c rootfs
			 7 - bitbake -p (rm -rf cache/ tmp/cache/)
			 8 - bitbake -p (rm -rf tmp/cache)
			 9 - bitbake -p
			10 - size of tmp dir
			11 - size of tmp dir (rm_work)
EOT
}

if [ $# -ne 5 ]
then
	usage
	exit 1
fi

while getopts "h:vf:" opt; do
	case $opt in
#case $1 in
		h)	usage
			exit 0
			;;
		v)	option=$2;
			shift;
			;;
		f)	INPUT_FILE1=$3;
			shift;
			INPUT_FILE2=$3;
			;;
		*)	usage
			exit 1
			;;
	esac
done

echo "#######"
echo $INPUT_FILE1
echo $INPUT_FILE2
echo "#######"

#check machine_type:
#read line < $INPUT_FILE1
#MACHINE1=`echo $line | cut -d ',' -f1`
#echo $MACHINE1
#read line < $INPUT_FILE2
#MACHINE2=`echo $line | cut -d ',' -f1`
#echo $MACHINE2

FN1=`echo $INPUT_FILE1 | cut -d '.' -f1`
FN2=`echo $INPUT_FILE2 | cut -d '.' -f1`


#backup and create json
echo $option

case $option in
	3)	build_type="bb-sato"
		;;
	4)	build_type="bb-kernel"
		;;
	5)	build_type="bb-sato-rmwork"
		;;
	6)	build_type="bb-sato-c-rootfs"
		;;
	7)	build_type="bb-p-cache-tmp"
		;;
	8)	build_type="bb-p-tmp"
		;;
	9)	build_type="bb-p"
		;;
	10)	build_type="size-tmp-dir"
		;;
	11)	build_type="size-tmp-dir-rmwork"
		;;
	*)	usage
		exit 0
		;;
esac

FN1=$FN1"_$build_type"
FN2=$FN2"_$build_type"

#backup
if [ ! -d "backup" ];
then
	mkdir "backup"
fi

if [ -f $FN1.json ];
then
        mv $FN1.json "./backup/$FN1-`date  +%Y%m%d%H%M%S`.json"
fi
if [ -f $FN2.json ]
then
        mv $FN2.json "./backup/$FN2-`date  +%Y%m%d%H%M%S`.json"
fi

python compute_json.py $option $INPUT_FILE1 > "$FN1.json"
if [ $? -ne 0 ]
then
	echo "Error on computing: $ compute_json.py $option $INPUT_FILE1"
	exit 1
fi
python compute_json.py $option $INPUT_FILE2 > "$FN2.json"
if [ $? -ne 0 ]
then
        echo "Error on computing: $ compute_json.py $option $INPUT_FILE22"
        exit 1
fi
