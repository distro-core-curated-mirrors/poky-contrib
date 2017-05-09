#!/bin/bash

CHROOT=debian-8

function umountIt {
    mDir=$1
    if mount|grep ${CHROOT} |grep  -q ${mDir} ;then
        echo " unmounting ${CHROOT}/${mDir} "
        umount /${CHROOT}/${mDir}
    fi
}

umountIt proc
umountIt dev
umountIt sys
umountIt tmp
