include xorg-driver-common.inc

DEPENDS += "inputproto kbproto "

<<<<<<< HEAD
python populate_packages_prepend() {
    add_abi_depends(d, "input")
}

=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
FILES_${PN} += " ${libdir}/xorg/modules/input/*.so"
FILES_${PN}-dbg += " ${libdir}/xorg/modules/input/.debug"
