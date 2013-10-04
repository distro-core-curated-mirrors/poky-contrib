SUMMARY = "Provider of the machine specific securetty file"
DESCRIPTION = "Provider of the machine specific securetty file"
SECTION = "base utils"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

INHIBIT_DEFAULT_DEPS = "1"

<<<<<<< HEAD
PR = "r2"

SRC_URI = "file://securetty"

# Since SERIAL_CONSOLES is likely to be set from the machine configuration
=======
PR = "r1"

SRC_URI = "file://securetty"

# Since we deduce our arch from ${SERIAL_CONSOLE}
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
PACKAGE_ARCH = "${MACHINE_ARCH}"

do_install () {
	# Ensure we add a suitable securetty file to the package that has
	# most common embedded TTYs defined.
<<<<<<< HEAD
	install -d ${D}${sysconfdir}
	install -m 0400 ${WORKDIR}/securetty ${D}${sysconfdir}/securetty
	if [ ! -z "${SERIAL_CONSOLES}" ]; then
		# Our SERIAL_CONSOLES contains a baud rate and sometimes extra
		# options as well. The following pearl :) takes that and converts
=======
	if [ ! -z "${SERIAL_CONSOLE}" ]; then
		# Our SERIAL_CONSOLE contains a baud rate and sometimes a -L
		# option as well. The following pearl :) takes that and converts
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
		# it into newline-separated tty's and appends them into
		# securetty. So if a machine has a weird looking console device
		# node (e.g. ttyAMA0) that securetty does not know, it will get
		# appended to securetty and root logins will be allowed on that
		# console.
<<<<<<< HEAD
		tmp="${SERIAL_CONSOLES}"
		for entry in $tmp ; do
			ttydev=`echo "$entry" | sed -e 's/^[0-9]*\;//' -e 's/\;.*//'`
			if ! grep -q $ttydev ${D}${sysconfdir}/securetty; then
				echo $ttydev >> ${D}${sysconfdir}/securetty
			fi
		done
	fi
=======
		echo "${SERIAL_CONSOLE}" | sed -e 's/[0-9][0-9]\|\-L//g'|tr "[ ]" "[\n]"  >> ${WORKDIR}/securetty
	fi
	install -d ${D}${sysconfdir}
	install -m 0400 ${WORKDIR}/securetty ${D}${sysconfdir}/securetty 
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
}
