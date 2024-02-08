FILESEXTRAPATHS:prepend := "${THISDIR}/glib-2.0:"

require glib-2.0_2.79.1.bb

#PACKAGECONFIG:remove = "introspection"
PACKAGECONFIG = ""
