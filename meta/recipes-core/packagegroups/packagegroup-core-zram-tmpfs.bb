SUMMARY = "Use zram for temporary directories instead of tmpfs"
PR = "r1"

inherit packagegroup

RDEPENDS:${PN} = " \
	util-linux-zramctl \
	e2fsprogs-mke2fs \
	"
