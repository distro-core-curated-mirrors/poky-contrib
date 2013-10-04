SUMMARY = "manage symlinks in /etc/rcN.d."
DESCRIPTION = "update-rc.d is a utilities that allows the management of symlinks to the initscripts in the /etc/rcN.d directory structure."
SECTION = "base"

LICENSE = "GPLv2+"
LIC_FILES_CHKSUM = "file://update-rc.d;beginline=5;endline=15;md5=148a48321b10eb37c1fa3ee02b940a75"

<<<<<<< HEAD
PR = "r5"
=======
PR = "r4"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

# Revision corresponding to tag update-rc.d_0.7
SRCREV = "eca680ddf28d024954895f59a241a622dd575c11"

<<<<<<< HEAD
SRC_URI = "git://github.com/philb/update-rc.d.git \
           file://add-verbose.patch \
           file://check-if-symlinks-are-valid.patch \
          "
=======
SRC_URI = "git://github.com/philb/update-rc.d.git;protocol=git \
           file://add-verbose.patch;"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

S = "${WORKDIR}/git"

inherit allarch

do_compile() {
}

do_install() {
	install -d ${D}${sbindir}
	install -m 0755 ${S}/update-rc.d ${D}${sbindir}/update-rc.d
}

BBCLASSEXTEND = "native"
