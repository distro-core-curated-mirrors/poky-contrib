include xorg-driver-common.inc

DEPENDS =+ "renderproto videoproto xextproto fontsproto"

<<<<<<< HEAD
python populate_packages_prepend() {
    add_abi_depends(d, "video")
}
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
