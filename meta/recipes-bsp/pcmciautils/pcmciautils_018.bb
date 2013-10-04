require pcmciautils.inc

SRC_URI += "file://makefile_fix.patch"

SRC_URI[md5sum] = "5d85669b3440baa4532363da6caaf1b4"
SRC_URI[sha256sum] = "79e6ae441278e178c07501d492394ed2c0326fdb66894f6d040ec811b0dc8ed5"

<<<<<<< HEAD
PR = "r1"

FILES_${PN}-dbg += "*/udev/.debug"
FILES_${PN} += "*/udev"
=======
PR = "r0"

FILES_${PN}-dbg += "${libdir}/udev/.debug"
FILES_${PN} += "${libdir}/udev"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
