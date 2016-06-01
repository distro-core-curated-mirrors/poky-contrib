#!/bin/bash
ME=$(basename $0)
INPUT_FILE=input.csv

# Usage

usage () {
cat << EOT
Usage: 	$ME [-h]
	$ME [-s] - bitbake core-image-sato
	$ME [-k] - bitbake virtual/kernel
	$ME [-r] - bitbake core-image-sato (rm_work)
	$ME [-P] - bitbake -p (rm -rf cache /tmp/cache/)
	$ME [-p] - bitbake -p
	$ME [-t] - size of tmp dir
	$ME [-T] - size of tmp dir (rm_work)

EOT
}


while getopts "h:s:k:r:p:P:t:T:" opt; do
	case $opt in
#case $1 in
		-h)	usage
			exit 0
			;;
		-s)	param=3
			file=core-image-sato.json
			;;
		-k)	param=4
			file=bbkernel.json
			;;
		-r)	param=5
			file=core-image-sato-rmw.json
			;;
		-P)	param=6
			file=rmcache.json
			;;
		-p)	param=7
			file=p.json
			;;
		-t)	param=8
			file=tmpdir.json
			;;
		-T)	param=9
			file=tmpdir_rmwork.json
			;;
		*)	usage
			exit 1
			;;
	esac
done

#check machine_type:
read line < $INPUT_FILE
MACHINE=`echo $line | cut -d ',' -f1`

#backup 
mv "$MACHINE-$file" "$MACHINE-$file-`date  +%Y%m%d%H%M%S`"
#create JSON by machine type
python compute_json.py $param > "$MACHINE-$file"
