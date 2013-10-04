require gdb-common.inc

<<<<<<< HEAD
DEPENDS = "expat-native ncurses-native readline-native"
=======
DEPENDS = "expat-native ncurses-native"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

EXTRA_OECONF += "--without-python"

#EXTRA_OEMAKE += "LDFLAGS='${BUILD_LDFLAGS}'"

GDBPROPREFIX = ""

inherit cross
inherit gettext

datadir .= "/gdb-${TUNE_PKGARCH}${TARGET_VENDOR}-${TARGET_OS}"
