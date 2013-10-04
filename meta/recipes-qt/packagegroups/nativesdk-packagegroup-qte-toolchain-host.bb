<<<<<<< HEAD
require nativesdk-packagegroup-qt-toolchain-host.inc

DESCRIPTION = "Host packages for Qt Embedded SDK"
=======
require recipes-core/packagegroups/nativesdk-packagegroup-sdk-host.bb

DESCRIPTION = "Host packages for Qt Embedded SDK"
LICENSE = "MIT"

RDEPENDS_${PN} += "nativesdk-qt4-tools"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
