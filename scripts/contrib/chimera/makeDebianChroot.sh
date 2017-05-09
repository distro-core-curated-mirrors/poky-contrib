#!/bin/bash

# this is largely pulled from
# http://www.linuxquestions.org/questions/debian-26/how-to-install-debian-using-debootstrap-4175465295/

CHROOT=debian-8

mkdir /${CHROOT}
wget --no-remove-listing -O /${CHROOT}/deboot.html -q http://ftp.us.debian.org/debian/pool/main/d/debootstrap
DEB=$(grep 'all.deb' /${CHROOT}/deboot.html | awk -F 'href' '{print $2}' | cut -d '"' -f2 | tail -1)
echo "using debootstrap deb $DEB"
wget -P /${CHROOT}/debootstrap http://ftp.us.debian.org/debian/pool/main/d/debootstrap/${DEB}
cd /${CHROOT}/debootstrap

echo "unpacking $DEB"
ar vx debootstrap_1.0.90_all.deb
tar xf data.tar.gz
ln -s /debian-8/debootstrap/usr/sbin/debootstrap /usr/sbin/debootstrap
ln -s /debian-8/debootstrap/usr/share/debootstrap/ /usr/share/debootstrap

echo "running debootstrap"
debootstrap --include linux-image-amd64,locales --arch amd64 unstable /${CHROOT}  http://ftp.us.debian.org/debian

# ubuntu version
# debootstrap --arch amd64 xenial /${CHROOT} http://archive.ubuntu.com/ubuntu
#cleanup
rm /usr/sbin/debootstrap /usr/share/debootstrap
cd ~
echo "To use do $chroot /debian-8 /bin/bash"
echo "or better ./goDebianChroot.sh "
echo "Then you are in debianland"
