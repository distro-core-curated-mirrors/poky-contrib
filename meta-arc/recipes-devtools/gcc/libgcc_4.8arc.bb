require recipes-devtools/gcc/gcc-4.8arc.inc
require recipes-devtools/gcc/libgcc.inc

do_install_append_libc-baremetal () {
	rmdir ${D}${base_libdir}
}

RDEPENDS_${PN}-dev_libc-baremetal = ""

COMPATIBLE_MACHINE = "arc"