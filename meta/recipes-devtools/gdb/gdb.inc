require gdb-common.inc

inherit gettext

SRC_URI += "file://kill_arm_map_symbols.patch \
            file://gdbserver-cflags-last.diff;striplevel=0 \
<<<<<<< HEAD
            file://renesas-sh-native-support.patch \
=======
	    file://renesas-sh-native-support.patch \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
           "
#LDFLAGS_append = " -s"
#export CFLAGS_append=" -L${STAGING_LIBDIR}"

# cross-canadian must not see this
PACKAGES =+ "gdbserver"
FILES_gdbserver = "${bindir}/gdbserver"
