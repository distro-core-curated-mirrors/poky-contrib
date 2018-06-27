#!/bin/sh

PATH=/sbin:/bin:/usr/sbin:/usr/bin

#ROOT_MOUNT="/rootfs"
#ROOT_IMAGE="rootfs.img"
#MOUNT="/bin/mount"
#UMOUNT="/bin/umount"
#ISOLINUX=""

#ROOT_DISK=""

early_setup() {
    mkdir -p /proc
    mkdir -p /sys
    mount -t proc proc /proc
    mount -t sysfs sysfs /sys
    mount -t devtmpfs none /dev

    # support modular kernel
    modprobe isofs 2> /dev/null

    mkdir -p /run
    mkdir -p /var/run

    #$_UDEV_DAEMON --daemon
    #udevadm trigger --action=add
}

read_args() {
    [ -z "$CMDLINE" ] && CMDLINE=`cat /proc/cmdline`
    for arg in $CMDLINE; do
        optarg=`expr "x$arg" : 'x[^=]*=\(.*\)'`
        case $arg in
            root=*)
                ROOT_DEVICE=$optarg ;;
            rootimage=*)
                ROOT_IMAGE=$optarg ;;
            rootfstype=*)
                modprobe $optarg 2> /dev/null ;;
            LABEL=*)
                label=$optarg ;;
            video=*)
                video_mode=$arg ;;
            vga=*)
                vga_mode=$arg ;;
            console=*)
                if [ -z "${console_params}" ]; then
                    console_params=$arg
                else
                    console_params="$console_params $arg"
                fi ;;
            debugshell*)
                if [ -z "$optarg" ]; then
                        shelltimeout=30
                else
                        shelltimeout=$optarg
                fi 
        esac
    done
}

fatal() {
    echo $1 >$CONSOLE
    echo >$CONSOLE
    exec sh
}

early_setup

[ -z "$CONSOLE" ] && CONSOLE="/dev/console"

read_args

echo "Booting Poky-Tiny..."
C=0
while true
do
  # don't wait for more than $shelltimeout seconds, if it's set
  if [ -n "$shelltimeout" ]; then
      echo -n " " $(( $shelltimeout - $C ))
      if [ $C -ge $shelltimeout ]; then
           echo "..."
	   echo "Mounted filesystems"
           mount | grep media
           echo "Available block devices"
           cat /proc/partitions
           echo ""
           fatal "Poky-Tiny Reference Distribution: "
      fi
      C=$(( C + 1 ))
  fi
  sleep 1
done
