#!/bin/bash

CHROOT=debian-8

function mountOrDie {
    mDir=$1
    if mount|grep ${CHROOT} |grep  -q ${mDir} ;then
        echo " ${mDir} mounted already, exiting..."
        exit
    else
        echo "not mounted so mounting ${mDir}"
        mount -o bind /${mDir} /${CHROOT}/${mDir}
    fi
}

mountOrDie tmp
mountOrDie proc
mountOrDie dev
mountOrDie sys


echo "jumping into chroot"
chroot /${CHROOT} /bin/bash
