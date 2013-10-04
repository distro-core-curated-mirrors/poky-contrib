SUMMARY = "Xorg minimal fonts data"
DESCRIPTION = "Minimal fonts required by X.org."
HOMEPAGE = "http://www.x.org"
BUGTRACKER = "n/a"

SECTION = "x11/fonts"

LICENSE = "PD"
<<<<<<< HEAD
LIC_FILES_CHKSUM = "file://../misc/fonts.dir;md5=82a143d94d6a974aafe97132d2d519ab \
=======
LIC_FILES_CHKSUM = "file://../misc/fonts.alias;md5=bbe8d3c0e4e74af96e3ac393985c4fbb \
                    file://../misc/fonts.dir;md5=82a143d94d6a974aafe97132d2d519ab \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
                    file://../misc/cursor.pcf.gz;md5=40bc81001fef4c21ca08df4305014a2a"

SRC_URI = "file://misc"

PE = "1"
<<<<<<< HEAD
PR = "r2"
=======
PR = "r1"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

inherit allarch

PACKAGES = "${PN}"
FILES_${PN} = "${libdir}/X11/ ${datadir}/fonts/X11/"
RDEPENDS_${PN} += "font-alias"

do_install() {
	install -d ${D}/${datadir}/fonts/X11/misc
	install -m 0644 ${WORKDIR}/misc/* ${D}/${datadir}/fonts/X11/misc/
	install -d ${D}/${libdir}/X11
	ln -sf ${datadir}/fonts/X11/ ${D}/${libdir}/X11/fonts -s
}
