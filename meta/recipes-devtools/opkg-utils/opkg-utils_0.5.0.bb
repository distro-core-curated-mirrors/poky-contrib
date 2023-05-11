SUMMARY = "Additional utilities for the opkg package manager"
SECTION = "base"
HOMEPAGE = "http://git.yoctoproject.org/cgit/cgit.cgi/opkg-utils"
LICENSE = "GPL-2.0-or-later"
LIC_FILES_CHKSUM = "file://COPYING;md5=94d55d512a9ba36caa9b7df079bae19f \
                    file://opkg.py;beginline=2;endline=18;md5=ffa11ff3c15eb31c6a7ceaa00cc9f986"

SRC_URI = "git://git.yoctoproject.org/opkg-utils;protocol=https;branch=master"
SRCREV = "9239541f14a2529b9d01c0a253ab11afa2822dab"

S = "${WORKDIR}/git"

RDEPENDS:${PN} += "bash opkg-update-alternatives"

inherit perlnative

# For native builds we use the host Python
PYTHONRDEPS = "python3 python3-shell python3-io python3-math python3-crypt python3-logging python3-fcntl python3-pickle python3-compression python3-stringold"
PYTHONRDEPS:class-native = ""

PACKAGECONFIG = "python"
PACKAGECONFIG[python] = ",,,${PYTHONRDEPS}"

do_install() {
	oe_runmake PREFIX=${prefix} DESTDIR=${D} install

	# update-alternatives is now packaged by opkg-update-alternatives
	rm -f ${D}${bindir}/update-alternatives

	# Remove python scripts if not enabled
	if ! ${@bb.utils.contains('PACKAGECONFIG', 'python', 'true', 'false', d)}; then
		grep -lZ "/usr/bin/env.*python" ${D}${bindir}/* | xargs -0 rm
	fi
}

# These are empty and will pull python3-dev into images where it wouldn't
# have been otherwise, so don't generate them.
PACKAGES:remove = "${PN}-dev ${PN}-staticdev"

BBCLASSEXTEND = "native nativesdk"

CLEANBROKEN = "1"
