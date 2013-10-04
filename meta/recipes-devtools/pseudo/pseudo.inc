# Note: Due to the bitbake wrapper script, making changes to pseudo can be
# difficult.  To work around the current version of the wrapper use:
# BBFETCH2=True PSEUDO_BUILD=1 ../bitbake/bin/bitbake pseudo-native [-c CMD]

DESCRIPTION = "Pseudo gives fake root capabilities to a normal user"
HOMEPAGE = "http://git.yoctoproject.org/cgit/cgit.cgi/pseudo"
LIC_FILES_CHKSUM = "file://COPYING;md5=243b725d71bb5df4a1e5920b344b86ad"
SECTION = "base"
LICENSE = "LGPL2.1"
DEPENDS = "sqlite3"

<<<<<<< HEAD
SRC_URI_append_class-nativesdk = " file://symver.patch"

SRC_URI_append_class-native = " file://symver.patch"
=======
SRC_URI_append_virtclass-nativesdk = " file://symver.patch"

SRC_URI_append_virtclass-native = " file://symver.patch"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

FILES_${PN} = "${libdir}/pseudo/lib*/libpseudo.so ${bindir}/* ${localstatedir}/pseudo ${prefix}/var/pseudo"
FILES_${PN}-dbg += "${libdir}/pseudo/lib*/.debug"
PROVIDES += "virtual/fakeroot"

MAKEOPTS = ""

inherit siteinfo

do_configure () {
	:
}

NO32LIBS ??= "1"
<<<<<<< HEAD
NO32LIBS_virtclass-nativesdk = "1"
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

# Compile for the local machine arch...
do_compile () {
	if [ "${SITEINFO_BITS}" = "64" ]; then
<<<<<<< HEAD
	  ${S}/configure ${PSEUDO_EXTRA_OPTS} --prefix=${prefix} --libdir=${prefix}/lib/pseudo/lib${SITEINFO_BITS} --with-sqlite-lib=${baselib} --with-sqlite=${STAGING_DIR_TARGET}${exec_prefix} --cflags="${CFLAGS}" --bits=${SITEINFO_BITS} --enable-static-sqlite --without-rpath
	else
	  ${S}/configure ${PSEUDO_EXTRA_OPTS} --prefix=${prefix} --libdir=${prefix}/lib/pseudo/lib --with-sqlite-lib=${baselib} --with-sqlite=${STAGING_DIR_TARGET}${exec_prefix} --cflags="${CFLAGS}" --bits=${SITEINFO_BITS} --enable-static-sqlite --without-rpath
	fi
	oe_runmake ${MAKEOPTS}
}

maybe_make32() {
	# We probably don't need to build 32-bit binaries.
	make32=false
	if [ "${SITEINFO_BITS}" = "64" ]; then
		case "${NO32LIBS}" in
		0)	make32=true
			;;
		1)	make32=false
			;;
		*)	# If unset, build 32-bit if we think we can.
			if [ -e "/usr/include/gnu/stubs-32.h" ]; then
				make32=true
			fi
			;;
		esac
	fi
	if $make32; then
		if ! [ -e "/usr/include/gnu/stubs-32.h" ]; then
			echo >&2 "WARNING: Can't find stubs-32.h, but usually need it to build 32-bit libpseudo."
			echo >&2 "If the build fails, install 32-bit developer packages."
			echo >&2 "If you are using 32-bit binaries, the 32-bit libpseudo is NOT optional."
		else
			echo "Attempting to build 32-bit libpseudo.so for ${PN}."
		fi
	else
		echo "Building/installing only 64-bit libpseudo.so for ${PN}."
		echo "If you need to run 32-bit executables, ensure that NO32LIBS is set to 0."
	fi
=======
	  ${S}/configure --prefix=${prefix} --libdir=${prefix}/lib/pseudo/lib${SITEINFO_BITS} --with-sqlite=${STAGING_DIR_TARGET}${exec_prefix} --cflags="${CFLAGS}" --bits=${SITEINFO_BITS} --enable-static-sqlite --without-rpath
	else
	  ${S}/configure --prefix=${prefix} --libdir=${prefix}/lib/pseudo/lib --with-sqlite=${STAGING_DIR_TARGET}${exec_prefix} --cflags="${CFLAGS}" --bits=${SITEINFO_BITS} --enable-static-sqlite --without-rpath
	fi
	oe_runmake ${MAKEOPTS}
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
}

# Two below are the same
# If necessary compile for the alternative machine arch.  This is only 
# necessary in a native build.
<<<<<<< HEAD
do_compile_prepend_class-native () {
	maybe_make32
	if $make32; then
		# We need the 32-bit libpseudo on a 64-bit machine...
		# Note that this is not well-tested outside of x86/x86_64.
=======
do_compile_prepend_virtclass-native () {
	if [ "${SITEINFO_BITS}" = "64" -a -e "/usr/include/gnu/stubs-32.h" -a "${PN}" = "pseudo-native" -a "${NO32LIBS}" != "1" ]; then
		# We need the 32-bit libpseudo on a 64-bit machine...
                # ... and we really, really, hope that the native host is
                # x86, or else --bits may not work.
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

		# if we're being rebuilt due to a dependency change, we need to make sure
		# everything is clean before we configure and build -- if we haven't previously
		# built this will fail and be ignored.
		make ${MAKEOPTS} distclean || :

<<<<<<< HEAD
		./configure ${PSEUDO_EXTRA_OPTS} --prefix=${prefix} --libdir=${prefix}/lib/pseudo/lib --with-sqlite-lib=${baselib} --with-sqlite=${STAGING_DIR_TARGET}${exec_prefix} --bits=32 --without-rpath
=======
		./configure --prefix=${prefix} --libdir=${prefix}/lib/pseudo/lib --with-sqlite=${STAGING_DIR_TARGET}${exec_prefix} --bits=32 --without-rpath
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
		oe_runmake ${MAKEOPTS} libpseudo
		# prevent it from removing the lib, but remove everything else
		make 'LIB=foo' ${MAKEOPTS} distclean 
	fi
}

<<<<<<< HEAD
do_compile_prepend_class-nativesdk () {
	maybe_make32
	if $make32; then
		# We need the 32-bit libpseudo on a 64-bit machine.
		# Note that this is not well-tested outside of x86/x86_64.
		./configure ${PSEUDO_EXTRA_OPTS} --prefix=${prefix} --libdir=${prefix}/lib/pseudo/lib --with-sqlite-lib=${baselib} --with-sqlite=${STAGING_DIR_TARGET}${exec_prefix} --bits=32 --without-rpath
=======
do_compile_prepend_virtclass-nativesdk () {
	if [ "${SITEINFO_BITS}" = "64" -a -e "/usr/include/gnu/stubs-32.h" -a "${PN}" = "pseudo-native" -a "${NO32LIBS}" != "1" ]; then
		# We need the 32-bit libpseudo on a 64-bit machine...
                # ... and we really, really, hope that the native host is
                # x86, or else --bits may not work.
		./configure --prefix=${prefix} --libdir=${prefix}/lib/pseudo/lib --with-sqlite=${STAGING_DIR_TARGET}${exec_prefix} --bits=32 --without-rpath
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
		oe_runmake ${MAKEOPTS} libpseudo
		# prevent it from removing the lib, but remove everything else
		make 'LIB=foo' ${MAKEOPTS} distclean 
	fi
}

do_install () {
	oe_runmake 'DESTDIR=${D}' ${MAKEOPTS} 'LIB=lib/pseudo/lib$(MARK64)' install
}

# Two below are the same
# If necessary install for the alternative machine arch.  This is only 
# necessary in a native build.
<<<<<<< HEAD
do_install_append_class-native () {
	maybe_make32
	if $make32; then
=======
do_install_append_virtclass-native () {
	if [ "${SITEINFO_BITS}" = "64" -a -e "/usr/include/gnu/stubs-32.h" -a "${PN}" = "pseudo-native" -a "${NO32LIBS}" != "1" ]; then
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
		mkdir -p ${D}${prefix}/lib/pseudo/lib
		cp lib/pseudo/lib/libpseudo.so ${D}${prefix}/lib/pseudo/lib/.
	fi
}

<<<<<<< HEAD
do_install_append_class-nativesdk () {
	maybe_make32
	if $make32; then
=======
do_install_append_virtclass-nativesdk () {
	if [ "${SITEINFO_BITS}" = "64" -a -e "/usr/include/gnu/stubs-32.h" -a "${PN}" = "pseudo-native" -a "${NO32LIBS}" != "1" ]; then
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
		mkdir -p ${D}${prefix}/lib/pseudo/lib
		cp lib/pseudo/lib/libpseudo.so ${D}${prefix}/lib/pseudo/lib/.
	fi
}

BBCLASSEXTEND = "native nativesdk"
