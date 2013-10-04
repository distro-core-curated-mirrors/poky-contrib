SUMMARY = "Liberation(tm) Fonts"
DESCRIPTION = "The Liberation(tm) Fonts is a font family originally \
created by Ascender(c) which aims at metric compatibility with \
Arial, Times New Roman, Courier New."
HOMEPAGE = "https://fedorahosted.org/liberation-fonts/"
BUGTRACKER = "https://bugzilla.redhat.com/"

SECTION = "x11/fonts"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=94d55d512a9ba36caa9b7df079bae19f"
RDEPENDS_${PN} = "fontconfig-utils"
<<<<<<< HEAD
PR = "r4"
PE = "1"

inherit fontcache

FONT_PACKAGES = "${PN}"
=======
PR = "r2"
PE = "1"

inherit allarch
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

SRC_URI = "https://fedorahosted.org/releases/l/i/liberation-fonts/liberation-fonts-${PV}.tar.gz \
           file://30-liberation-aliases.conf"

SRC_URI[md5sum] = "4846797ef0fc70b0cbaede2514677c58"
SRC_URI[sha256sum] = "0e0d0957c85b758561a3d4aef4ebcd2c39959e5328429d96ae106249d83531a1"

do_install () {
	install -d ${D}${datadir}/fonts/ttf/
	for i in *.ttf; do
		install -m 0644 $i ${D}${prefix}/share/fonts/ttf/${i}
	done

	install -d ${D}${sysconfdir}/fonts/conf.d/
	install -m 0644 ${WORKDIR}/30-liberation-aliases.conf ${D}${sysconfdir}/fonts/conf.d/

<<<<<<< HEAD
	install -d ${D}${prefix}/share/doc/${BPN}/
	install -m 0644 License.txt ${D}${datadir}/doc/${BPN}/
=======
	install -d ${D}${prefix}/share/doc/${PN}/
	install -m 0644 License.txt ${D}${datadir}/doc/${PN}/
}

pkg_postinst_${PN} () {
#!/bin/sh
if [ "x$D" != "x" ] ; then
	exit 1
fi
fc-cache
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
}

PACKAGES = "${PN}"
FILES_${PN} += "${sysconfdir} ${datadir}"
