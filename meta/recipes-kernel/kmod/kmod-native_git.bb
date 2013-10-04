# Copyright (C) 2012 Khem Raj <raj.khem@gmail.com>
# Released under the MIT license (see COPYING.MIT for the terms)

require kmod.inc
inherit native

<<<<<<< HEAD
SRC_URI += "file://fix-undefined-O_CLOEXEC.patch \
            file://0001-Fix-build-with-older-gcc-4.6.patch \
           "
=======
PR = "${INC_PR}.1"
SRC_URI += "file://fix-undefined-O_CLOEXEC.patch"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

do_install_append (){
	for tool in depmod insmod lsmod modinfo modprobe rmmod
	do
		ln -s kmod ${D}${bindir}/$tool
	done
}
