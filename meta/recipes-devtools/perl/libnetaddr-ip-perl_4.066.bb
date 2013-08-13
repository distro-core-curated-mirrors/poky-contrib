DESCRIPTION = "Perl module to manage IPv4 and IPv6 addresses and subnets"
SECTION = "libs"
LICENSE = "GPLv2"
RDEPENDS_${PN} += "perl-module-test-more"
BBCLASSEXTEND = "native"

PR = "r2"

SRC_URI = "http://search.cpan.org/CPAN/authors/id/M/MI/MIKER/NetAddr-IP-${PV}.tar.gz"
SRC_URI[md5sum] = "7c6cf77d3c02fa0baf77b6a97f2a670a"
SRC_URI[sha256sum] = "7f6f55395fd4226387f07864846aee47060e66ed6418bdc3be2b6e46b855ce14"

LIC_FILES_CHKSUM = "file://Copying;md5=cde580764a0fbc0f02fafde4c65d6227"

S = "${WORKDIR}/NetAddr-IP-${PV}"

inherit cpan

do_configure_prepend() {
	cd Lite/Util
	bbnote Executing autoreconf --verbose --install --force
        mkdir -p m4
        autoreconf -Wcross --verbose --install --force || bbfatal "autoreconf execution failed."
	./configure --build=${BUILD_SYS} --host=${HOST_SYS} \
		--target=${TARGET_SYS} --prefix=${prefix} --exec_prefix=${exec_prefix} \
		--bindir=${bindir} --sbindir=${sbindir} --libexecdir=${libexecdir} \
		--datadir=${datadir} --sysconfdir=${sysconfdir} \
		--sharedstatedir=${sharedstatedir} --localstatedir=${localstatedir} \
		--libdir=${libdir} --includedir=${includedir} \
		--oldincludedir=${oldincludedir} --infodir=${infodir} --mandir=${mandir}
	cd ${S}
}
