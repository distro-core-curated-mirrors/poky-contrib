<<<<<<< HEAD
inherit useradd_base

=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
# base-passwd-cross provides the default passwd and group files in the
# target sysroot, and shadow -native and -sysroot provide the utilities
# and support files needed to add and modify user and group accounts
DEPENDS_append = "${USERADDDEPENDS}"
USERADDDEPENDS = " base-passwd shadow-native shadow-sysroot shadow"
USERADDDEPENDS_virtclass-cross = ""
<<<<<<< HEAD
USERADDDEPENDS_class-native = ""
USERADDDEPENDS_class-nativesdk = ""
=======
USERADDDEPENDS_virtclass-native = ""
USERADDDEPENDS_virtclass-nativesdk = ""
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

# This preinstall function can be run in four different contexts:
#
# a) Before do_install
# b) At do_populate_sysroot_setscene when installing from sstate packages
# c) As the preinst script in the target package at do_rootfs time
# d) As the preinst script in the target package on device as a package upgrade
#
useradd_preinst () {
OPT=""
SYSROOT=""

if test "x$D" != "x"; then
	# Installing into a sysroot
	SYSROOT="$D"
	OPT="--root $D"

	# Add groups and users defined for all recipe packages
<<<<<<< HEAD
	GROUPADD_PARAM="${@get_all_cmd_params(d, 'groupadd')}"
	USERADD_PARAM="${@get_all_cmd_params(d, 'useradd')}"
	GROUPMEMS_PARAM="${@get_all_cmd_params(d, 'groupmems')}"
=======
	GROUPADD_PARAM="${@get_all_cmd_params(d, 'group')}"
	USERADD_PARAM="${@get_all_cmd_params(d, 'user')}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
else
	# Installing onto a target
	# Add groups and users defined only for this package
	GROUPADD_PARAM="${GROUPADD_PARAM}"
	USERADD_PARAM="${USERADD_PARAM}"
<<<<<<< HEAD
	GROUPMEMS_PARAM="${GROUPMEMS_PARAM}"
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
fi

# Perform group additions first, since user additions may depend
# on these groups existing
if test "x$GROUPADD_PARAM" != "x"; then
	echo "Running groupadd commands..."
	# Invoke multiple instances of groupadd for parameter lists
	# separated by ';'
	opts=`echo "$GROUPADD_PARAM" | cut -d ';' -f 1`
	remaining=`echo "$GROUPADD_PARAM" | cut -d ';' -f 2-`
	while test "x$opts" != "x"; do
<<<<<<< HEAD
		perform_groupadd "$SYSROOT" "$OPT $opts" 10
=======
		groupname=`echo "$opts" | awk '{ print $NF }'`
		group_exists=`grep "^$groupname:" $SYSROOT/etc/group || true`
		if test "x$group_exists" = "x"; then
			count=1
			while true; do
				eval $PSEUDO groupadd $OPT $opts || true
				group_exists=`grep "^$groupname:" $SYSROOT/etc/group || true`
				if test "x$group_exists" = "x"; then
					# File locking issues can require us to retry the command
					echo "WARNING: groupadd command did not succeed. Retrying..."
					sleep 1
				else
					break
				fi
				count=`expr $count + 1`
				if test $count = 11; then
					echo "ERROR: tried running groupadd command 10 times without success, giving up"
					exit 1
				fi
			done		
		else
			echo "Note: group $groupname already exists, not re-creating it"
		fi

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
		if test "x$opts" = "x$remaining"; then
			break
		fi
		opts=`echo "$remaining" | cut -d ';' -f 1`
		remaining=`echo "$remaining" | cut -d ';' -f 2-`
	done
fi 

if test "x$USERADD_PARAM" != "x"; then
	echo "Running useradd commands..."
	# Invoke multiple instances of useradd for parameter lists
	# separated by ';'
	opts=`echo "$USERADD_PARAM" | cut -d ';' -f 1`
	remaining=`echo "$USERADD_PARAM" | cut -d ';' -f 2-`
	while test "x$opts" != "x"; do
<<<<<<< HEAD
		perform_useradd "$SYSROOT" "$OPT $opts" 10
		if test "x$opts" = "x$remaining"; then
			break
		fi
		opts=`echo "$remaining" | cut -d ';' -f 1`
		remaining=`echo "$remaining" | cut -d ';' -f 2-`
	done
fi

if test "x$GROUPMEMS_PARAM" != "x"; then
	echo "Running groupmems commands..."
	# Invoke multiple instances of groupmems for parameter lists
	# separated by ';'
	opts=`echo "$GROUPMEMS_PARAM" | cut -d ';' -f 1`
	remaining=`echo "$GROUPMEMS_PARAM" | cut -d ';' -f 2-`
	while test "x$opts" != "x"; do
		perform_groupmems "$SYSROOT" "$OPT $opts" 10
=======
		# useradd does not have a -f option, so we have to check if the
		# username already exists manually
		username=`echo "$opts" | awk '{ print $NF }'`
		user_exists=`grep "^$username:" $SYSROOT/etc/passwd || true`
		if test "x$user_exists" = "x"; then
			count=1
			while true; do
				eval $PSEUDO useradd $OPT $opts || true
				user_exists=`grep "^$username:" $SYSROOT/etc/passwd || true`
				if test "x$user_exists" = "x"; then
					# File locking issues can require us to retry the command
					echo "WARNING: useradd command did not succeed. Retrying..."
					sleep 1
				else
					break
				fi
				count=`expr $count + 1`
				if test $count = 11; then
					echo "ERROR: tried running useradd command 10 times without success, giving up"
					exit 1
				fi
			done
		else
			echo "Note: username $username already exists, not re-creating it"
		fi

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
		if test "x$opts" = "x$remaining"; then
			break
		fi
		opts=`echo "$remaining" | cut -d ';' -f 1`
		remaining=`echo "$remaining" | cut -d ';' -f 2-`
	done
fi
}

useradd_sysroot () {
	# Pseudo may (do_install) or may not (do_populate_sysroot_setscene) be running 
	# at this point so we're explicit about the environment so pseudo can load if 
	# not already present.
	export PSEUDO="${FAKEROOTENV} PSEUDO_LOCALSTATEDIR=${STAGING_DIR_TARGET}${localstatedir}/pseudo ${STAGING_DIR_NATIVE}${bindir}/pseudo"

	# Explicitly set $D since it isn't set to anything
	# before do_install
	D=${STAGING_DIR_TARGET}
	useradd_preinst
}

useradd_sysroot_sstate () {
<<<<<<< HEAD
	if [ "${BB_CURRENTTASK}" = "package_setscene" -o "${BB_CURRENTTASK}" = "populate_sysroot_setscene" ]
=======
	if [ "${BB_CURRENTTASK}" = "package_setscene" ]
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
	then
		useradd_sysroot
	fi
}

do_install[prefuncs] += "${SYSROOTFUNC}"
SYSROOTFUNC = "useradd_sysroot"
SYSROOTFUNC_virtclass-cross = ""
<<<<<<< HEAD
SYSROOTFUNC_class-native = ""
SYSROOTFUNC_class-nativesdk = ""
SSTATEPREINSTFUNCS += "${SYSROOTPOSTFUNC}"
SYSROOTPOSTFUNC = "useradd_sysroot_sstate"
SYSROOTPOSTFUNC_virtclass-cross = ""
SYSROOTPOSTFUNC_class-native = ""
SYSROOTPOSTFUNC_class-nativesdk = ""

USERADDSETSCENEDEPS = "${MLPREFIX}base-passwd:do_populate_sysroot_setscene shadow-native:do_populate_sysroot_setscene ${MLPREFIX}shadow-sysroot:do_populate_sysroot_setscene"
USERADDSETSCENEDEPS_virtclass-cross = ""
USERADDSETSCENEDEPS_class-native = ""
USERADDSETSCENEDEPS_class-nativesdk = ""
do_package_setscene[depends] += "${USERADDSETSCENEDEPS}"
do_populate_sysroot_setscene[depends] += "${USERADDSETSCENEDEPS}"
=======
SYSROOTFUNC_virtclass-native = ""
SYSROOTFUNC_virtclass-nativesdk = ""
SSTATEPREINSTFUNCS += "${SYSROOTPOSTFUNC}"
SYSROOTPOSTFUNC = "useradd_sysroot_sstate"
SYSROOTPOSTFUNC_virtclass-cross = ""
SYSROOTPOSTFUNC_virtclass-native = ""
SYSROOTPOSTFUNC_virtclass-nativesdk = ""

USERADDSETSCENEDEPS = "${MLPREFIX}base-passwd:do_populate_sysroot_setscene shadow-native:do_populate_sysroot_setscene ${MLPREFIX}shadow-sysroot:do_populate_sysroot_setscene"
USERADDSETSCENEDEPS_virtclass-cross = ""
USERADDSETSCENEDEPS_virtclass-native = ""
USERADDSETSCENEDEPS_virtclass-nativesdk = ""
do_package_setscene[depends] = "${USERADDSETSCENEDEPS}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

# Recipe parse-time sanity checks
def update_useradd_after_parse(d):
    useradd_packages = d.getVar('USERADD_PACKAGES', True)

    if not useradd_packages:
<<<<<<< HEAD
        raise bb.build.FuncFailed("%s inherits useradd but doesn't set USERADD_PACKAGES" % d.getVar('FILE'))

    for pkg in useradd_packages.split():
        if not d.getVar('USERADD_PARAM_%s' % pkg, True) and not d.getVar('GROUPADD_PARAM_%s' % pkg, True) and not d.getVar('GROUPMEMS_PARAM_%s' % pkg, True):
            bb.fatal("%s inherits useradd but doesn't set USERADD_PARAM, GROUPADD_PARAM or GROUPMEMS_PARAM for package %s" % (d.getVar('FILE'), pkg))
=======
        raise bb.build.FuncFailed, "%s inherits useradd but doesn't set USERADD_PACKAGES" % d.getVar('FILE')

    for pkg in useradd_packages.split():
        if not d.getVar('USERADD_PARAM_%s' % pkg, True) and not d.getVar('GROUPADD_PARAM_%s' % pkg, True):
            raise bb.build.FuncFailed, "%s inherits useradd but doesn't set USERADD_PARAM or GROUPADD_PARAM for package %s" % (d.getVar('FILE'), pkg)
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

python __anonymous() {
    update_useradd_after_parse(d)
}

# Return a single [GROUP|USER]ADD_PARAM formatted string which includes the
# [group|user]add parameters for all USERADD_PACKAGES in this recipe
def get_all_cmd_params(d, cmd_type):
    import string
    
<<<<<<< HEAD
    param_type = cmd_type.upper() + "_PARAM_%s"
=======
    param_type = cmd_type.upper() + "ADD_PARAM_%s"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    params = []

    useradd_packages = d.getVar('USERADD_PACKAGES', True) or ""
    for pkg in useradd_packages.split():
        param = d.getVar(param_type % pkg, True)
        if param:
            params.append(param)

<<<<<<< HEAD
    return "; ".join(params)
=======
    return string.join(params, "; ")
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

# Adds the preinst script into generated packages
fakeroot python populate_packages_prepend () {
    def update_useradd_package(pkg):
        bb.debug(1, 'adding user/group calls to preinst for %s' % pkg)

        """
        useradd preinst is appended here because pkg_preinst may be
        required to execute on the target. Not doing so may cause
        useradd preinst to be invoked twice, causing unwanted warnings.
        """
        preinst = d.getVar('pkg_preinst_%s' % pkg, True) or d.getVar('pkg_preinst', True)
        if not preinst:
            preinst = '#!/bin/sh\n'
<<<<<<< HEAD
        preinst += 'bbnote () {\n%s}\n' % d.getVar('bbnote', True)
        preinst += 'bbwarn () {\n%s}\n' % d.getVar('bbwarn', True)
        preinst += 'bbfatal () {\n%s}\n' % d.getVar('bbfatal', True)
        preinst += 'perform_groupadd () {\n%s}\n' % d.getVar('perform_groupadd', True)
        preinst += 'perform_useradd () {\n%s}\n' % d.getVar('perform_useradd', True)
        preinst += 'perform_groupmems () {\n%s}\n' % d.getVar('perform_groupmems', True)
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        preinst += d.getVar('useradd_preinst', True)
        d.setVar('pkg_preinst_%s' % pkg, preinst)

        # RDEPENDS setup
        rdepends = d.getVar("RDEPENDS_%s" % pkg, True) or ""
        rdepends += ' ' + d.getVar('MLPREFIX') + 'base-passwd'
        rdepends += ' ' + d.getVar('MLPREFIX') + 'shadow'
        d.setVar("RDEPENDS_%s" % pkg, rdepends)

    # Add the user/group preinstall scripts and RDEPENDS requirements
    # to packages specified by USERADD_PACKAGES
    if not bb.data.inherits_class('nativesdk', d):
        useradd_packages = d.getVar('USERADD_PACKAGES', True) or ""
        for pkg in useradd_packages.split():
            update_useradd_package(pkg)
}
