#
# Records history of build output in order to detect regressions
#
# Based in part on testlab.bbclass and packagehistory.bbclass
#
# Copyright (C) 2011-2016 Intel Corporation
# Copyright (C) 2007-2011 Koen Kooi <koen@openembedded.org>
#

BUILDHISTORY_FEATURES ?= "image package sdk"
BUILDHISTORY_DIR ?= "${TOPDIR}/buildhistory"


def bh_classes_for_features(d):
    features = (d.getVar('BUILDHISTORY_FEATURES') or '').split()
    return ' '.join('buildhistory-{0}'.format(feature) for feature in features)


inherit ${@bh_classes_for_features(d)}

# Setting this to non-empty will remove the old content of the buildhistory as part of
# the current bitbake invocation and replace it with information about what was built
# during the build.
#
# This is meant to be used in continuous integration (CI) systems when invoking bitbake
# for full world builds. The effect in that case is that information about packages
# that no longer get build also gets removed from the buildhistory, which is not
# the case otherwise.
#
# The advantage over manually cleaning the buildhistory outside of bitbake is that
# the "version-going-backwards" check still works. When relying on that, be careful
# about failed world builds: they will lead to incomplete information in the
# buildhistory because information about packages that could not be built will
# also get removed. A CI system should handle that by discarding the buildhistory
# of failed builds.
#
# The expected usage is via auto.conf, but passing via the command line also works
# with: BB_ENV_EXTRAWHITE=BUILDHISTORY_RESET BUILDHISTORY_RESET=1
BUILDHISTORY_RESET ?= ""

BUILDHISTORY_OLD_DIR = "${BUILDHISTORY_DIR}/${@ "old" if "${BUILDHISTORY_RESET}" else ""}"
BUILDHISTORY_COMMIT ?= "1"
BUILDHISTORY_COMMIT_AUTHOR ?= "buildhistory <buildhistory@${DISTRO}>"
BUILDHISTORY_PUSH_REPO ?= ""

PATCH_GIT_USER_EMAIL ?= "buildhistory@oe"
PATCH_GIT_USER_NAME ?= "OpenEmbedded"

#
# rootfs_type can be: image, sdk_target, sdk_host
#
def buildhistory_list_installed(d, rootfs_type="image"):
    from oe.rootfs import image_list_installed_packages
    from oe.sdk import sdk_list_installed_packages
    from oe.utils import format_pkg_list

    process_list = [('file', 'bh_installed_pkgs.txt'),\
                    ('deps', 'bh_installed_pkgs_deps.txt')]

    if rootfs_type == "image":
        pkgs = image_list_installed_packages(d)
    else:
        pkgs = sdk_list_installed_packages(d, rootfs_type == "sdk_target")

    for output_type, output_file in process_list:
        output_file_full = os.path.join(d.getVar('WORKDIR'), output_file)

        with open(output_file_full, 'w') as output:
            output.write(format_pkg_list(pkgs, output_type))

buildhistory_get_installed() {
	mkdir -p $1

	# Get list of installed packages
	pkgcache="$1/installed-packages.tmp"
	cat ${WORKDIR}/bh_installed_pkgs.txt | sort > $pkgcache && rm ${WORKDIR}/bh_installed_pkgs.txt

	cat $pkgcache | awk '{ print $1 }' > $1/installed-package-names.txt
	if [ -s $pkgcache ] ; then
		cat $pkgcache | awk '{ print $2 }' | xargs -n1 basename > $1/installed-packages.txt
	else
		printf "" > $1/installed-packages.txt
	fi

	# Produce dependency graph
	# First, quote each name to handle characters that cause issues for dot
	sed 's:\([^| ]*\):"\1":g' ${WORKDIR}/bh_installed_pkgs_deps.txt > $1/depends.tmp &&
		rm ${WORKDIR}/bh_installed_pkgs_deps.txt
	# Remove lines with rpmlib(...) and config(...) dependencies, change the
	# delimiter from pipe to "->", set the style for recommend lines and
	# turn versioned dependencies into edge labels.
	sed -i -e '/rpmlib(/d' \
	       -e '/config(/d' \
	       -e 's:|: -> :' \
	       -e 's:"\[REC\]":[style=dotted]:' \
	       -e 's:"\([<>=]\+\)" "\([^"]*\)":[label="\1 \2"]:' \
		$1/depends.tmp
	# Add header, sorted and de-duped contents and footer and then delete the temp file
	printf "digraph depends {\n    node [shape=plaintext]\n" > $1/depends.dot
	cat $1/depends.tmp | sort -u >> $1/depends.dot
	echo "}" >>  $1/depends.dot
	rm $1/depends.tmp

	# Produce installed package sizes list
	oe-pkgdata-util -p ${PKGDATA_DIR} read-value "PKGSIZE" -n -f $pkgcache > $1/installed-package-sizes.tmp
	cat $1/installed-package-sizes.tmp | awk '{print $2 "\tKiB\t" $1}' | sort -n -r > $1/installed-package-sizes.txt
	rm $1/installed-package-sizes.tmp

	# We're now done with the cache, delete it
	rm $pkgcache

	if [ "$2" != "sdk" ] ; then
		# Produce some cut-down graphs (for readability)
		grep -v kernel-image $1/depends.dot | grep -v kernel-3 | grep -v kernel-4 > $1/depends-nokernel.dot
		grep -v libc6 $1/depends-nokernel.dot | grep -v libgcc > $1/depends-nokernel-nolibc.dot
		grep -v update- $1/depends-nokernel-nolibc.dot > $1/depends-nokernel-nolibc-noupdate.dot
		grep -v kernel-module $1/depends-nokernel-nolibc-noupdate.dot > $1/depends-nokernel-nolibc-noupdate-nomodules.dot
	fi

	# add complementary package information
	if [ -e ${WORKDIR}/complementary_pkgs.txt ]; then
		cp ${WORKDIR}/complementary_pkgs.txt $1
	fi
}

buildhistory_list_files() {
	# List the files in the specified directory, but exclude date/time etc.
	# This is somewhat messy, but handles where the size is not printed for device files under pseudo
	( cd $1
	find_cmd='find . ! -path . -printf "%M %-10u %-10g %10s %p -> %l\n"'
	if [ "$3" = "fakeroot" ] ; then
		eval ${FAKEROOTENV} ${FAKEROOTCMD} $find_cmd
	else
		eval $find_cmd
	fi | sort -k5 | sed 's/ * -> $//' > $2 )
}

buildhistory_list_files_no_owners() {
	# List the files in the specified directory, but exclude date/time etc.
	# Also don't output the ownership data, but instead output just - - so
	# that the same parsing code as for _list_files works.
	# This is somewhat messy, but handles where the size is not printed for device files under pseudo
	( cd $1
	find_cmd='find . ! -path . -printf "%M -          -          %10s %p -> %l\n"'
	if [ "$3" = "fakeroot" ] ; then
		eval ${FAKEROOTENV} ${FAKEROOTCMD} "$find_cmd"
	else
		eval "$find_cmd"
	fi | sort -k5 | sed 's/ * -> $//' > $2 )
}

def buildhistory_get_build_id(d):
    if d.getVar('BB_WORKERCONTEXT') != '1':
        return ""
    localdata = bb.data.createCopy(d)
    statuslines = []
    for func in oe.data.typed_value('BUILDCFG_FUNCS', localdata):
        g = globals()
        if func not in g:
            bb.warn("Build configuration function '%s' does not exist" % func)
        else:
            flines = g[func](localdata)
            if flines:
                statuslines.extend(flines)

    statusheader = d.getVar('BUILDCFG_HEADER')
    return('\n%s\n%s\n' % (statusheader, '\n'.join(statuslines)))

def buildhistory_get_modified(path):
    # copied from get_layer_git_status() in image-buildinfo.bbclass
    import subprocess
    try:
        subprocess.check_output("""cd %s; export PSEUDO_UNLOAD=1; set -e;
                                git diff --quiet --no-ext-diff
                                git diff --quiet --no-ext-diff --cached""" % path,
                                shell=True,
                                stderr=subprocess.STDOUT)
        return ""
    except subprocess.CalledProcessError as ex:
        # Silently treat errors as "modified", without checking for the
        # (expected) return code 1 in a modified git repo. For example, we get
        # output and a 129 return code when a layer isn't a git repo at all.
        return " -- modified"

def buildhistory_get_metadata_revs(d):
    # We want an easily machine-readable format here, so get_layers_branch_rev isn't quite what we want
    layers = (d.getVar("BBLAYERS") or "").split()
    medadata_revs = ["%-17s = %s:%s%s" % (os.path.basename(i), \
        base_get_metadata_git_branch(i, None).strip(), \
        base_get_metadata_git_revision(i, None), \
        buildhistory_get_modified(i)) \
            for i in layers]
    return '\n'.join(medadata_revs)

def outputvars(vars, listvars, d):
    vars = vars.split()
    listvars = listvars.split()
    ret = ""
    for var in vars:
        value = d.getVar(var) or ""
        if var in listvars:
            # Squash out spaces
            value = oe.utils.squashspaces(value)
        ret += "%s = %s\n" % (var, value)
    return ret.rstrip('\n')

def buildhistory_get_cmdline(d):
    argv = d.getVar('BB_CMDLINE', False)
    if argv:
        if argv[0].endswith('bin/bitbake'):
            bincmd = 'bitbake'
        else:
            bincmd = argv[0]
        return '%s %s' % (bincmd, ' '.join(argv[1:]))
    return ''


buildhistory_single_commit() {
	if [ "$3" = "" ] ; then
		commitopts="${BUILDHISTORY_DIR}/ --allow-empty"
		shortlogprefix="No changes: "
	else
		commitopts=""
		shortlogprefix=""
	fi
	if [ "${BUILDHISTORY_BUILD_FAILURES}" = "0" ] ; then
		result="succeeded"
	else
		result="failed"
	fi
	case ${BUILDHISTORY_BUILD_INTERRUPTED} in
		1)
			result="$result (interrupted)"
			;;
		2)
			result="$result (force interrupted)"
			;;
	esac
	commitmsgfile=`mktemp`
	cat > $commitmsgfile << END
${shortlogprefix}Build ${BUILDNAME} of ${DISTRO} ${DISTRO_VERSION} for machine ${MACHINE} on $2

cmd: $1

result: $result

metadata revisions:
END
	cat ${BUILDHISTORY_DIR}/metadata-revs >> $commitmsgfile
	git commit $commitopts -F $commitmsgfile --author "${BUILDHISTORY_COMMIT_AUTHOR}" > /dev/null
	rm $commitmsgfile
}

buildhistory_commit() {
	if [ ! -d ${BUILDHISTORY_DIR} ] ; then
		# Code above that creates this dir never executed, so there can't be anything to commit
		return
	fi

	# Create a machine-readable list of metadata revisions for each layer
	cat > ${BUILDHISTORY_DIR}/metadata-revs <<END
${@buildhistory_get_metadata_revs(d)}
END

	( cd ${BUILDHISTORY_DIR}/
		# Initialise the repo if necessary
		if [ ! -e .git ] ; then
			git init -q
		else
			git tag -f build-minus-3 build-minus-2 > /dev/null 2>&1 || true
			git tag -f build-minus-2 build-minus-1 > /dev/null 2>&1 || true
			git tag -f build-minus-1 > /dev/null 2>&1 || true
		fi

		check_git_config

		# Check if there are new/changed files to commit (other than metadata-revs)
		repostatus=`git status --porcelain | grep -v " metadata-revs$"`
		HOSTNAME=`hostname 2>/dev/null || echo unknown`
		CMDLINE="${@buildhistory_get_cmdline(d)}"
		if [ "$repostatus" != "" ] ; then
			git add -A .
			# porcelain output looks like "?? packages/foo/bar"
			# Ensure we commit metadata-revs with the first commit
			buildhistory_single_commit "$CMDLINE" "$HOSTNAME" dummy
			git gc --auto --quiet
		else
			buildhistory_single_commit "$CMDLINE" "$HOSTNAME"
		fi
		if [ "${BUILDHISTORY_PUSH_REPO}" != "" ] ; then
			git push -q ${BUILDHISTORY_PUSH_REPO}
		fi) || true
}

BUILDHISTORY_COMMIT_PREFUNCS ?= ""

python buildhistory_eventhandler() {
    if e.data.getVar('BUILDHISTORY_FEATURES').strip():
        reset = e.data.getVar("BUILDHISTORY_RESET")
        olddir = e.data.getVar("BUILDHISTORY_OLD_DIR")
        if isinstance(e, bb.event.BuildStarted):
            if reset:
                import shutil
                # Clean up after potentially interrupted build.
                if os.path.isdir(olddir):
                    shutil.rmtree(olddir)
                rootdir = e.data.getVar("BUILDHISTORY_DIR")
                entries = [ x for x in os.listdir(rootdir) if not x.startswith('.') ]
                bb.utils.mkdirhier(olddir)
                for entry in entries:
                    os.rename(os.path.join(rootdir, entry),
                              os.path.join(olddir, entry))
        elif isinstance(e, bb.event.BuildCompleted):
            if reset:
                import shutil
                shutil.rmtree(olddir)
            if e.data.getVar("BUILDHISTORY_COMMIT") == "1":
                bb.note("Writing buildhistory")
                for func in (d.getVar("BUILDHISTORY_COMMIT_PREFUNCS") or "").split():
                    bb.build.exec_func(func, d)
                import time
                start=time.time()
                localdata = bb.data.createCopy(e.data)
                localdata.setVar('BUILDHISTORY_BUILD_FAILURES', str(e._failures))
                interrupted = getattr(e, '_interrupted', 0)
                localdata.setVar('BUILDHISTORY_BUILD_INTERRUPTED', str(interrupted))
                bb.build.exec_func("buildhistory_commit", localdata)
                stop=time.time()
                bb.note("Writing buildhistory took: %s seconds" % round(stop-start))
            else:
                bb.note("No commit since BUILDHISTORY_COMMIT != '1'")
}

addhandler buildhistory_eventhandler
buildhistory_eventhandler[eventmask] = "bb.event.BuildCompleted bb.event.BuildStarted"

#TODO: Move to buildhistory-image.bbclass?
do_testimage[postfuncs] += "write_ptest_result"
do_testimage[vardepsexclude] += "write_ptest_result"

python write_ptest_result() {
    write_latest_ptest_result(d, d.getVar('BUILDHISTORY_DIR'))
}

def write_latest_ptest_result(d, histdir):
    import glob
    import subprocess
    test_log_dir = d.getVar('TEST_LOG_DIR')
    input_ptest = os.path.join(test_log_dir, 'ptest_log')
    output_ptest = os.path.join(histdir, 'ptest')
    if os.path.exists(input_ptest):
        try:
            # Lock it avoid race issue
            lock = bb.utils.lockfile(output_ptest + "/ptest.lock")
            bb.utils.mkdirhier(output_ptest)
            oe.path.copytree(input_ptest, output_ptest)
            # Sort test result
            for result in glob.glob('%s/pass.fail.*' % output_ptest):
                bb.debug(1, 'Processing %s' % result)
                cmd = ['sort', result, '-o', result]
                bb.debug(1, 'Running %s' % cmd)
                ret = subprocess.call(cmd)
                if ret != 0:
                    bb.error('Failed to run %s!' % cmd)
        finally:
            bb.utils.unlockfile(lock)
