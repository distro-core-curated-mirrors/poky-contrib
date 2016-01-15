#!/bin/sh

ARGS="$@"

ANYFAILED=no
echo "START: $0"

run_ptest(){
    
    for libdir in $1
    do
        [ ! -d "$libdir" ] && continue
        for x in `ls -d $libdir*/ptest 2>/dev/null`
        do
            [ ! -f $x/run-ptest ] && continue
            [ -h `dirname $x` ] && continue
            date "+%Y-%m-%dT%H:%M"
            echo "BEGIN: $x"
            cd "$x"
            timeout 20m ./run-ptest || ANYFAILED=yes
            echo "END: $x"
            date "+%Y-%m-%dT%H:%M"
        done
    done
    echo "STOP: $0"
    if [ "$ANYFAILED" = "yes"  ]; then
        exit 1
    fi
}

if [ "$#" -lt 1 ]; then
    run_ptest '/usr/lib/*'
else
    run_ptest /usr/lib/${ARGS}
fi
exit 0
