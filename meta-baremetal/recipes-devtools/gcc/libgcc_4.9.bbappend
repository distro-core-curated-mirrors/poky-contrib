do_install_append_libc-baremetal () {
	rmdir ${D}${base_libdir}
}

RDEPENDS_${PN}-dev_libc-baremetal = ""
