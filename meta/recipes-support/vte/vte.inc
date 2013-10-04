DESCRIPTION = "vte is a virtual terminal emulator"
BUGTRACKER = "https://bugzilla.gnome.org/buglist.cgi?product=vte"
LICENSE = "LGPLv2.1+"
DEPENDS = " glib-2.0 gtk+ intltool-native ncurses gobject-introspection-stub"
RDEPENDS_libvte = "vte-termcap"

inherit gnome gtk-doc

EXTRA_OECONF = "--disable-python --disable-introspection"

PACKAGES =+ "libvte vte-termcap"
FILES_libvte = "${libdir}/*.so.* ${libexecdir}/gnome-pty-helper"
<<<<<<< HEAD
FILES_${PN}-dbg =+ "${libexecdir}/.debug ${prefix}/src ${bindir}/.debug \
               ${libdir}/.debug"
FILES_vte-termcap = "${datadir}/vte/termcap-0.0"

=======
FILES_vte-dbg =+ "${libexecdir}/.debug"
FILES_vte-termcap = "${datadir}/vte/termcap-0.0"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
