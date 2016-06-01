#!/bin/bash


#IF1="input-ubuntu.csv"
#IF2="input-fedora.csv"
usage () {
cat << EOT
Usage:  $ME [-h]
        $ME <file1> <file2>]


EOT
}


bash jgen.sh -v 3 -f $0 $1
echo $?
bash jgen.sh -v 4 -f $0 $1
echo $?
bash jgen.sh -v 5 -f $0 $1
echo $?
bash jgen.sh -v 6 -f $0 $1
echo $?
bash jgen.sh -v 7 -f $0 $1
echo $?
bash jgen.sh -v 8 -f $0 $1
echo $?
bash jgen.sh -v 9 -f $0 $1
echo $?
