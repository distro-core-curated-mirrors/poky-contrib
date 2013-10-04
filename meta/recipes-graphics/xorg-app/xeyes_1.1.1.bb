require xorg-app-common.inc
<<<<<<< HEAD

SUMMARY = "X11 eyes that follow the mouse cursor demo"
DESCRIPTION = "Xeyes is a small X11 application that shows a pair of eyes that move to \
follow the location of the mouse cursor around the screen."

=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
PE = "1"

LIC_FILES_CHKSUM = "file://COPYING;md5=3ea51b365051ac32d1813a7dbaa4bfc6"

SRC_URI[md5sum] = "a3035dcecdbdb89e864177c080924981"
SRC_URI[sha256sum] = "975e98680cd59e1f9439016386609546ed08c284d0f05a95276f96aca6e8a521"

<<<<<<< HEAD
DEPENDS += " virtual/libx11 libxau libxt libxext libxmu libxrender"
=======
DEPENDS += " virtual/libx11 libxau libxt libxext libxmu"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
