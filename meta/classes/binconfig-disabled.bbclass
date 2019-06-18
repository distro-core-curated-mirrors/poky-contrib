#
# Class to disable binconfig files instead of installing them.  The config files
# on the target are still usable, only the sysroot is disabled.
#

inherit binconfig

# The list of scripts which should be disabled, for example ${bindir}/foo-config.
BINCONFIG ?= ""

# This replaces the function in binconfig.bbclass to stub out instead of mangle
# the sysroot config scripts.
binconfig_sysroot_preprocess () {
	for x in ${BINCONFIG}; do
		# Only write a stub if the config actually exists, as some recipes list
		# all *potential* names.
		if [ -x ${D}$x ]; then
			install -d ${SYSROOT_DESTDIR}${bindir_crossscripts}
			configname=`basename $x`
			# Make the disabled script emit invalid parameters for those configure
			# scripts which call it without checking the return code.
			cat <<- EOF >${SYSROOT_DESTDIR}${bindir_crossscripts}/$configname
			#!/bin/sh
			echo 'ERROR: $configname should not be used, use an alternative such as pkg-config' >&2
			echo '--should-not-have-used-$configname'
			exit 1
			EOF
			chmod +x ${SYSROOT_DESTDIR}${bindir_crossscripts}/$configname
		fi
	done
}
