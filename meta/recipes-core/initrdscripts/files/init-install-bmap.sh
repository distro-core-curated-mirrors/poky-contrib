#!/bin/sh -e
#
# Copyright (c) 2012, Intel Corporation.
# Copyright (c) 2022, Konsulko Group.
# All rights reserved.
#
# install-bmap.sh [device_name] [image_name]
#

PATH=/sbin:/bin:/usr/sbin:/usr/bin

DEBUG=1

check() {
    rc=0
    echo; echo -n "$1"
    $2 1>/dev/null 2>err || rc=$?
    if [ $rc = 0 ]; then
	echo " [OK]"
    else
	echo " [FAIL]"
	cat err
	echo; echo "*********************"
	echo "Installation aborted."
	echo "*********************"
	if [ $DEBUG = 1 ]; then
	    echo; echo ">>> Fallback to /bin/sh for debugging"
	    /bin/sh
	fi
	exit 1
    fi
}

# Make sure we have a .bmap file for the image
if [ ! -e /run/media/$1/$2 -o ! -e /run/media/$1/$2.bmap ]; then
	    echo "This installer requires an <image> file and an <image>.bmap file. Installation aborted."
	    exit 1
fi

# Get a list of hard drives
hdnamelist=""
live_dev_name=`cat /proc/mounts | grep ${1%/} | awk '{print $1}'`
live_dev_name=${live_dev_name#\/dev/}
# Only strip the digit identifier if the device is not an mmc
case $live_dev_name in
    mmcblk*)
    ;;
    nvme*)
    ;;
    *)
        live_dev_name=${live_dev_name%%[0-9]*}
    ;;
esac

echo "Searching for hard drives ..."

# Some eMMC devices have special sub devices such as mmcblk0boot0 etc
# we're currently only interested in the root device so pick them wisely
devices=`ls /sys/block/ | grep -v mmcblk` || true
mmc_devices=`ls /sys/block/ | grep "mmcblk[0-9]\{1,\}$"` || true
devices="$devices $mmc_devices"

for device in $devices; do
    case $device in
        loop*)
            # skip loop device
            ;;
        sr*)
            # skip CDROM device
            ;;
        ram*)
            # skip ram device
            ;;
        *)
            # skip the device LiveOS is on
            # Add valid hard drive name to the list
            case $device in
                $live_dev_name*)
                # skip the device we are running from
                ;;
                *)
                    hdnamelist="$hdnamelist $device"
                ;;
            esac
            ;;
    esac
done

if [ -z "${hdnamelist}" ]; then
    echo "You need another device (besides the live device /dev/${live_dev_name}) to install the image. Installation aborted."
    exit 1
fi

TARGET_DEVICE_NAME=""
for hdname in $hdnamelist; do
    # Display found hard drives and their basic info
    echo "-------------------------------"
    echo /dev/$hdname
    if [ -r /sys/block/$hdname/device/vendor ]; then
        echo -n "VENDOR="
        cat /sys/block/$hdname/device/vendor
    fi
    if [ -r /sys/block/$hdname/device/model ]; then
        echo -n "MODEL="
        cat /sys/block/$hdname/device/model
    fi
    if [ -r /sys/block/$hdname/device/uevent ]; then
        echo -n "UEVENT="
        cat /sys/block/$hdname/device/uevent
    fi
    echo
done

# Get user choice
while true; do
    echo "Please select an install target or press n to exit ($hdnamelist ): "
    read answer
    if [ "$answer" = "n" ]; then
        echo "Installation manually aborted."
        exit 1
    fi
    for hdname in $hdnamelist; do
        if [ "$answer" = "$hdname" ]; then
            TARGET_DEVICE_NAME=$answer
            break
        fi
    done
    if [ -n "$TARGET_DEVICE_NAME" ]; then
        break
    fi
done

if [ -n "$TARGET_DEVICE_NAME" ]; then
    echo "Installing image on /dev/$TARGET_DEVICE_NAME ..."
else
    echo "No hard drive selected. Installation aborted."
    exit 1
fi

device=/dev/$TARGET_DEVICE_NAME

#
# The udev automounter can cause pain here, kill it
#
rm -f /etc/udev/rules.d/automount.rules
rm -f /etc/udev/scripts/mount*

#
# Unmount anything the automounter had mounted
#
umount ${device}* 2> /dev/null || /bin/true

mkdir -p /tmp

# Create /etc/mtab if not present
if [ ! -e /etc/mtab ] && [ -e /proc/mounts ]; then
    ln -sf /proc/mounts /etc/mtab
fi

disk_size=$(parted ${device} unit mb print | grep '^Disk .*: .*MB' | cut -d" " -f 3 | sed -e "s/MB//")

# MMC devices are special in a couple of ways
# 1) they use a partition prefix character 'p'
# 2) they are detected asynchronously (need rootwait)
rootwait=""
part_prefix=""
if [ ! "${device#/dev/mmcblk}" = "${device}" ] || \
   [ ! "${device#/dev/nvme}" = "${device}" ]; then
    part_prefix="p"
    rootwait="rootwait"
fi

# USB devices also require rootwait
if [ -n `readlink /dev/disk/by-id/usb* | grep $TARGET_DEVICE_NAME` ]; then
    rootwait="rootwait"
fi

echo "*****************"
echo "Disk size:   $disk_size MB ($device)"
echo "*****************"
check "Deleting partition table on ${device} ..." "sgdisk --zap-all ${device}"
#dd if=/dev/zero of=${device} bs=512 count=35

check "Creating new partition table on ${device} ..." "parted ${device} -s mklabel gpt"

echo; echo "Copying ${2} with bmaptool to ${device} ..."
bmaptool copy /run/media/${1}/${2} ${device}
if [ $? = 0 ]; then
    echo "[OK]"
fi
sync

partprobe ${device} >/dev/null
echo; echo "Correcting Alternate GPT header location ..."
sgdisk --move-second-header ${device}
partprobe ${device} >/dev/null

last_part=$(partx -rgo NR -n -1:-1 "${device}")
check "Resize last partition (${device}${part_prefix}${last_part}) ..." "parted ${device} -s resizepart ${last_part} 100%"

partprobe ${device} >/dev/null
#check "Resize the file system of the last partition (${device}${part_prefix}${last_part}) ..." "resize2fs ${device}${part_prefix}${last_part}" 

echo; echo "Final partition table for ${device}"
sgdisk -p ${device}

sync

echo; echo "Installation successful. Remove your installation media and press ENTER to reboot."

read enter

echo "Rebooting..."
reboot -f
