SUMMARY = "Use zram-backed swap"
PR = "r1"

inherit packagegroup

RDEPENDS:${PN} = " \
	util-linux-zramctl \
	util-linux-swaponoff \
	util-linux-mkswap \
	"
