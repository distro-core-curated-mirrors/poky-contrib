inherit rootfs_${IMAGE_PKGTYPE}

# Only Linux SDKs support populate_sdk_ext, fall back to populate_sdk
# in the non-Linux SDK_OS case, such as mingw32
SDKEXTCLASS ?= "${@['populate_sdk', 'populate_sdk_ext']['linux' in d.getVar("SDK_OS")]}"
inherit ${SDKEXTCLASS}

TOOLCHAIN_TARGET_TASK += "${PACKAGE_INSTALL}"
TOOLCHAIN_TARGET_TASK_ATTEMPTONLY += "${PACKAGE_INSTALL_ATTEMPTONLY}"
POPULATE_SDK_POST_TARGET_COMMAND += "rootfs_sysroot_relativelinks; "

inherit gzipnative

LICENSE = "MIT"
PACKAGES = ""
DEPENDS += "${MLPREFIX}qemuwrapper-cross depmodwrapper-cross"
RDEPENDS += "${PACKAGE_INSTALL} ${LINGUAS_INSTALL}"
RRECOMMENDS += "${PACKAGE_INSTALL_ATTEMPTONLY}"

INHIBIT_DEFAULT_DEPS = "1"

TESTIMAGECLASS = "${@base_conditional('TEST_IMAGE', '1', 'testimage-auto', '', d)}"
inherit ${TESTIMAGECLASS}

# IMAGE_FEATURES may contain any available package group
IMAGE_FEATURES ?= ""
IMAGE_FEATURES[type] = "list"
IMAGE_FEATURES[validitems] += "debug-tweaks read-only-rootfs empty-root-password allow-empty-password post-install-logging"

# Generate companion debugfs?
IMAGE_GEN_DEBUGFS ?= "0"

# rootfs bootstrap install
ROOTFS_BOOTSTRAP_INSTALL = "${@bb.utils.contains("IMAGE_FEATURES", "package-management", "", "${ROOTFS_PKGMANAGE_BOOTSTRAP}",d)}"

# These packages will be removed from a read-only rootfs after all other
# packages have been installed
ROOTFS_RO_UNNEEDED = "update-rc.d base-passwd shadow ${VIRTUAL-RUNTIME_update-alternatives} ${ROOTFS_BOOTSTRAP_INSTALL}"

# packages to install from features
FEATURE_INSTALL = "${@' '.join(oe.packagegroup.required_packages(oe.data.typed_value('IMAGE_FEATURES', d), d))}"
FEATURE_INSTALL[vardepvalue] = "${FEATURE_INSTALL}"
FEATURE_INSTALL_OPTIONAL = "${@' '.join(oe.packagegroup.optional_packages(oe.data.typed_value('IMAGE_FEATURES', d), d))}"
FEATURE_INSTALL_OPTIONAL[vardepvalue] = "${FEATURE_INSTALL_OPTIONAL}"

# Define some very basic feature package groups
FEATURE_PACKAGES_package-management = "${ROOTFS_PKGMANAGE}"
SPLASH ?= "psplash"
FEATURE_PACKAGES_splash = "${SPLASH}"

IMAGE_INSTALL_COMPLEMENTARY = '${@complementary_globs("IMAGE_FEATURES", d)}'

def check_image_features(d):
    valid_features = (d.getVarFlag('IMAGE_FEATURES', 'validitems') or "").split()
    valid_features += d.getVarFlags('COMPLEMENTARY_GLOB').keys()
    for var in d:
       if var.startswith("PACKAGE_GROUP_"):
           bb.warn("PACKAGE_GROUP is deprecated, please use FEATURE_PACKAGES instead")
           valid_features.append(var[14:])
       elif var.startswith("FEATURE_PACKAGES_"):
           valid_features.append(var[17:])
    valid_features.sort()

    features = set(oe.data.typed_value('IMAGE_FEATURES', d))
    for feature in features:
        if feature not in valid_features:
            if bb.utils.contains('EXTRA_IMAGE_FEATURES', feature, True, False, d):
                raise bb.parse.SkipRecipe("'%s' in IMAGE_FEATURES (added via EXTRA_IMAGE_FEATURES) is not a valid image feature. Valid features: %s" % (feature, ' '.join(valid_features)))
            else:
                raise bb.parse.SkipRecipe("'%s' in IMAGE_FEATURES is not a valid image feature. Valid features: %s" % (feature, ' '.join(valid_features)))

IMAGE_INSTALL ?= ""
IMAGE_INSTALL[type] = "list"
export PACKAGE_INSTALL ?= "${IMAGE_INSTALL} ${ROOTFS_BOOTSTRAP_INSTALL} ${FEATURE_INSTALL}"
PACKAGE_INSTALL_ATTEMPTONLY ?= "${FEATURE_INSTALL_OPTIONAL}"

IMGDEPLOYDIR = "${WORKDIR}/deploy-${PN}-image-complete"

# Images are generally built explicitly, do not need to be part of world.
EXCLUDE_FROM_WORLD = "1"

USE_DEVFS ?= "1"
USE_DEPMOD ?= "1"

PID = "${@os.getpid()}"

PACKAGE_ARCH = "${MACHINE_ARCH}"

LDCONFIGDEPEND ?= "ldconfig-native:do_populate_sysroot"
LDCONFIGDEPEND_libc-uclibc = ""
LDCONFIGDEPEND_libc-musl = ""

# This is needed to have depmod data in PKGDATA_DIR,
# but if you're building small initramfs image
# e.g. to include it in your kernel, you probably
# don't want this dependency, which is causing dependency loop
KERNELDEPMODDEPEND ?= "virtual/kernel:do_packagedata"

# POPULATESYSROOTDEPS fails to expand correctly with multilibs since overrides aren't set for image.bbclass
# we don't need these depends so just clear them
do_populate_sysroot[depends] = ""

do_rootfs[depends] += " \
    makedevs-native:do_populate_sysroot virtual/fakeroot-native:do_populate_sysroot ${LDCONFIGDEPEND} \
    virtual/update-alternatives-native:do_populate_sysroot update-rc.d-native:do_populate_sysroot \
    ${KERNELDEPMODDEPEND} \
"
do_rootfs[recrdeptask] += "do_packagedata"

def rootfs_command_variables(d):
    return ['ROOTFS_POSTPROCESS_COMMAND','ROOTFS_PREPROCESS_COMMAND','ROOTFS_POSTINSTALL_COMMAND','ROOTFS_POSTUNINSTALL_COMMAND','OPKG_PREPROCESS_COMMANDS','OPKG_POSTPROCESS_COMMANDS','IMAGE_POSTPROCESS_COMMAND',
            'IMAGE_PREPROCESS_COMMAND','RPM_PREPROCESS_COMMANDS','RPM_POSTPROCESS_COMMANDS','DEB_PREPROCESS_COMMANDS','DEB_POSTPROCESS_COMMANDS']

python () {
    variables = rootfs_command_variables(d) + sdk_command_variables(d)
    for var in variables:
        if d.getVar(var, False):
            d.setVarFlag(var, 'func', '1')
}

def rootfs_variables(d):
    from oe.rootfs import variable_depends
    variables = ['IMAGE_DEVICE_TABLE','IMAGE_DEVICE_TABLES','BUILD_IMAGES_FROM_FEEDS','IMAGE_TYPES_MASKED','IMAGE_ROOTFS_ALIGNMENT','IMAGE_OVERHEAD_FACTOR','IMAGE_ROOTFS_SIZE','IMAGE_ROOTFS_EXTRA_SPACE',
                 'IMAGE_ROOTFS_MAXSIZE','IMAGE_NAME','IMAGE_LINK_NAME','IMAGE_MANIFEST','DEPLOY_DIR_IMAGE','IMAGE_FSTYPES','IMAGE_INSTALL_COMPLEMENTARY','IMAGE_LINGUAS',
                 'MULTILIBRE_ALLOW_REP','MULTILIB_TEMP_ROOTFS','MULTILIB_VARIANTS','MULTILIBS','ALL_MULTILIB_PACKAGE_ARCHS','MULTILIB_GLOBAL_VARIANTS','BAD_RECOMMENDATIONS','NO_RECOMMENDATIONS',
                 'PACKAGE_ARCHS','PACKAGE_CLASSES','TARGET_VENDOR','TARGET_ARCH','TARGET_OS','OVERRIDES','BBEXTENDVARIANT','FEED_DEPLOYDIR_BASE_URI','INTERCEPT_DIR','USE_DEVFS',
                 'CONVERSIONTYPES', 'IMAGE_GEN_DEBUGFS', 'ROOTFS_RO_UNNEEDED', 'IMGDEPLOYDIR', 'PACKAGE_EXCLUDE_COMPLEMENTARY']
    variables.extend(rootfs_command_variables(d))
    variables.extend(variable_depends(d))
    return " ".join(variables)

do_rootfs[vardeps] += "${@rootfs_variables(d)}"

do_build[depends] += "virtual/kernel:do_deploy"

def build_live(d):
    if bb.utils.contains("IMAGE_FSTYPES", "live", "live", "0", d) == "0": # live is not set but hob might set iso or hddimg
        d.setVar('NOISO', bb.utils.contains('IMAGE_FSTYPES', "iso", "0", "1", d))
        d.setVar('NOHDD', bb.utils.contains('IMAGE_FSTYPES', "hddimg", "0", "1", d))
        if d.getVar('NOISO') == "0" or d.getVar('NOHDD') == "0":
            return "image-live"
        return ""
    return "image-live"

IMAGE_TYPE_live = "${@build_live(d)}"
inherit ${IMAGE_TYPE_live}

IMAGE_TYPE_vm = '${@bb.utils.contains_any("IMAGE_FSTYPES", ["vmdk", "vdi", "qcow2", "hdddirect"], "image-vm", "", d)}'
inherit ${IMAGE_TYPE_vm}

def build_uboot(d):
    if 'u-boot' in (d.getVar('IMAGE_FSTYPES') or ''):
        return "image_types_uboot"
    else:
        return ""

IMAGE_TYPE_uboot = "${@build_uboot(d)}"
inherit ${IMAGE_TYPE_uboot}

python () {
    deps = " " + imagetypes_getdepends(d)
    d.appendVarFlag('do_rootfs', 'depends', deps)

    deps = ""
    for dep in (d.getVar('EXTRA_IMAGEDEPENDS') or "").split():
        deps += " %s:do_populate_sysroot" % dep
    d.appendVarFlag('do_build', 'depends', deps)

    #process IMAGE_FEATURES, we must do this before runtime_mapping_rename
    #Check for replaces image features
    features = set(oe.data.typed_value('IMAGE_FEATURES', d))
    remain_features = features.copy()
    for feature in features:
        replaces = set((d.getVar("IMAGE_FEATURES_REPLACES_%s" % feature) or "").split())
        remain_features -= replaces

    #Check for conflict image features
    for feature in remain_features:
        conflicts = set((d.getVar("IMAGE_FEATURES_CONFLICTS_%s" % feature) or "").split())
        temp = conflicts & remain_features
        if temp:
            bb.fatal("%s contains conflicting IMAGE_FEATURES %s %s" % (d.getVar('PN'), feature, ' '.join(list(temp))))

    d.setVar('IMAGE_FEATURES', ' '.join(sorted(list(remain_features))))

    check_image_features(d)
    initramfs_image = d.getVar('INITRAMFS_IMAGE') or ""
    if initramfs_image != "":
        d.appendVarFlag('do_build', 'depends', " %s:do_bundle_initramfs" %  d.getVar('PN'))
        d.appendVarFlag('do_bundle_initramfs', 'depends', " %s:do_image_complete" % initramfs_image)
}

IMAGE_CLASSES += "image_types"
inherit ${IMAGE_CLASSES}

IMAGE_POSTPROCESS_COMMAND ?= ""

# some default locales
IMAGE_LINGUAS ?= "de-de fr-fr en-gb"

LINGUAS_INSTALL ?= "${@" ".join(map(lambda s: "locale-base-%s" % s, d.getVar('IMAGE_LINGUAS').split()))}"

# Prefer image, but use the fallback files for lookups if the image ones
# aren't yet available.
PSEUDO_PASSWD = "${IMAGE_ROOTFS}:${STAGING_DIR_NATIVE}"

inherit rootfs-postcommands

PACKAGE_EXCLUDE ??= ""
PACKAGE_EXCLUDE[type] = "list"

fakeroot python do_rootfs () {
    from oe.rootfs import create_rootfs
    from oe.manifest import create_manifest
    import logging

    logger = d.getVar('BB_TASK_LOGGER', False)
    if logger:
        logcatcher = bb.utils.LogCatcher()
        logger.addHandler(logcatcher)
    else:
        logcatcher = None

    # NOTE: if you add, remove or significantly refactor the stages of this
    # process then you should recalculate the weightings here. This is quite
    # easy to do - just change the MultiStageProgressReporter line temporarily
    # to pass debug=True as the last parameter and you'll get a printout of
    # the weightings as well as a map to the lines where next_stage() was
    # called. Of course this isn't critical, but it helps to keep the progress
    # reporting accurate.
    stage_weights = [1, 203, 354, 186, 65, 4228, 1, 353, 49, 330, 382, 23, 1]
    progress_reporter = bb.progress.MultiStageProgressReporter(d, stage_weights)
    progress_reporter.next_stage()

    # Handle package exclusions
    excl_pkgs = d.getVar("PACKAGE_EXCLUDE").split()
    inst_pkgs = d.getVar("PACKAGE_INSTALL").split()
    inst_attempt_pkgs = d.getVar("PACKAGE_INSTALL_ATTEMPTONLY").split()

    d.setVar('PACKAGE_INSTALL_ORIG', ' '.join(inst_pkgs))
    d.setVar('PACKAGE_INSTALL_ATTEMPTONLY', ' '.join(inst_attempt_pkgs))

    for pkg in excl_pkgs:
        if pkg in inst_pkgs:
            bb.warn("Package %s, set to be excluded, is in %s PACKAGE_INSTALL (%s).  It will be removed from the list." % (pkg, d.getVar('PN'), inst_pkgs))
            inst_pkgs.remove(pkg)

        if pkg in inst_attempt_pkgs:
            bb.warn("Package %s, set to be excluded, is in %s PACKAGE_INSTALL_ATTEMPTONLY (%s).  It will be removed from the list." % (pkg, d.getVar('PN'), inst_pkgs))
            inst_attempt_pkgs.remove(pkg)

    d.setVar("PACKAGE_INSTALL", ' '.join(inst_pkgs))
    d.setVar("PACKAGE_INSTALL_ATTEMPTONLY", ' '.join(inst_attempt_pkgs))

    # Ensure we handle package name remapping
    # We have to delay the runtime_mapping_rename until just before rootfs runs
    # otherwise, the multilib renaming could step in and squash any fixups that
    # may have occurred.
    pn = d.getVar('PN')
    runtime_mapping_rename("PACKAGE_INSTALL", pn, d)
    runtime_mapping_rename("PACKAGE_INSTALL_ATTEMPTONLY", pn, d)
    runtime_mapping_rename("BAD_RECOMMENDATIONS", pn, d)

    # Generate the initial manifest
    create_manifest(d)

    progress_reporter.next_stage()

    # generate rootfs
    create_rootfs(d, progress_reporter=progress_reporter, logcatcher=logcatcher)

    progress_reporter.finish()
}
do_rootfs[dirs] = "${TOPDIR}"
do_rootfs[cleandirs] += "${S} ${IMGDEPLOYDIR}"
do_rootfs[umask] = "022"
addtask rootfs before do_build after do_prepare_recipe_sysroot

fakeroot python do_image () {
    from oe.utils import execute_pre_post_process

    pre_process_cmds = d.getVar("IMAGE_PREPROCESS_COMMAND")

    execute_pre_post_process(d, pre_process_cmds)
}
do_image[dirs] = "${TOPDIR}"
do_image[umask] = "022"
addtask do_image after do_rootfs before do_build

fakeroot python do_image_complete () {
    from oe.utils import execute_pre_post_process

    post_process_cmds = d.getVar("IMAGE_POSTPROCESS_COMMAND")

    execute_pre_post_process(d, post_process_cmds)
}
do_image_complete[dirs] = "${TOPDIR}"
do_image_complete[umask] = "022"
SSTATETASKS += "do_image_complete"
SSTATE_SKIP_CREATION_task-image-complete = '1'
do_image_complete[sstate-inputdirs] = "${IMGDEPLOYDIR}"
do_image_complete[sstate-outputdirs] = "${DEPLOY_DIR_IMAGE}"
do_image_complete[stamp-extra-info] = "${MACHINE}"
addtask do_image_complete after do_image before do_build

# Add image-level QA/sanity checks to IMAGE_QA_COMMANDS
#
# IMAGE_QA_COMMANDS += " \
#     image_check_everything_ok \
# "
# This task runs all functions in IMAGE_QA_COMMANDS after the image
# construction has completed in order to validate the resulting image.
fakeroot python do_image_qa () {
    from oe.utils import ImageQAFailed

    qa_cmds = (d.getVar('IMAGE_QA_COMMANDS') or '').split()
    qamsg = ""

    for cmd in qa_cmds:
        try:
            bb.build.exec_func(cmd, d)
        except oe.utils.ImageQAFailed as e:
            qamsg = qamsg + '\tImage QA function %s failed: %s\n' % (e.name, e.description)
        except bb.build.FuncFailed as e:
            qamsg = qamsg + '\tImage QA function %s failed' % e.name
            if e.logfile:
                qamsg = qamsg + ' (log file is located at %s)' % e.logfile
            qamsg = qamsg + '\n'

    if qamsg:
        imgname = d.getVar('IMAGE_NAME')
        bb.fatal("QA errors found whilst validating image: %s\n%s" % (imgname, qamsg))
}
addtask do_image_qa after do_image_complete before do_build

#
# Write environment variables used by wic
# to tmp/sysroots/<machine>/imgdata/<image>.env
#
python do_rootfs_wicenv () {
    wicvars = d.getVar('WICVARS')
    if not wicvars:
        return

    stdir = d.getVar('STAGING_DIR')
    outdir = os.path.join(stdir, 'imgdata')
    bb.utils.mkdirhier(outdir)
    basename = d.getVar('IMAGE_BASENAME')
    with open(os.path.join(outdir, basename) + '.env', 'w') as envf:
        for var in wicvars.split():
            value = d.getVar(var)
            if value:
                envf.write('%s="%s"\n' % (var, value.strip()))
}
addtask do_rootfs_wicenv after do_image before do_image_wic
do_rootfs_wicenv[vardeps] += "${WICVARS}"
do_rootfs_wicenv[prefuncs] = 'set_image_size'

def setup_debugfs_variables(d):
    d.appendVar('IMAGE_ROOTFS', '-dbg')
    d.appendVar('IMAGE_LINK_NAME', '-dbg')
    d.appendVar('IMAGE_NAME','-dbg')
    d.setVar('IMAGE_BUILDING_DEBUGFS', 'true')
    debugfs_image_fstypes = d.getVar('IMAGE_FSTYPES_DEBUGFS')
    if debugfs_image_fstypes:
        d.setVar('IMAGE_FSTYPES', debugfs_image_fstypes)

python setup_debugfs () {
    setup_debugfs_variables(d)
}

python () {
    vardeps = set()
    # We allow CONVERSIONTYPES to have duplicates. That avoids breaking
    # derived distros when OE-core or some other layer independently adds
    # the same type. There is still only one command for each type, but
    # presumably the commands will do the same when the type is the same,
    # even when added in different places.
    #
    # Without de-duplication, gen_conversion_cmds() below
    # would create the same compression command multiple times.
    ctypes = set(d.getVar('CONVERSIONTYPES').split())
    old_overrides = d.getVar('OVERRIDES', False)

    def _image_base_type(type):
        basetype = type
        for ctype in ctypes:
            if type.endswith("." + ctype):
                basetype = type[:-len("." + ctype)]
                break

        if basetype != type:
            # New base type itself might be generated by a conversion command.
            basetype = _image_base_type(basetype)

        return basetype

    basetypes = {}
    alltypes = d.getVar('IMAGE_FSTYPES').split()
    typedeps = {}

    if d.getVar('IMAGE_GEN_DEBUGFS') == "1":
        debugfs_fstypes = d.getVar('IMAGE_FSTYPES_DEBUGFS').split()
        for t in debugfs_fstypes:
            alltypes.append("debugfs_" + t)

    def _add_type(t):
        baset = _image_base_type(t)
        input_t = t
        if baset not in basetypes:
            basetypes[baset]= []
        if t not in basetypes[baset]:
            basetypes[baset].append(t)
        debug = ""
        if t.startswith("debugfs_"):
            t = t[8:]
            debug = "debugfs_"
        deps = (d.getVar('IMAGE_TYPEDEP_' + t) or "").split()
        vardeps.add('IMAGE_TYPEDEP_' + t)
        if baset not in typedeps:
            typedeps[baset] = set()
        deps = [debug + dep for dep in deps]
        for dep in deps:
            if dep not in alltypes:
                alltypes.append(dep)
            _add_type(dep)
            basedep = _image_base_type(dep)
            typedeps[baset].add(basedep)

        if baset != input_t:
            _add_type(baset)

    for t in alltypes[:]:
        _add_type(t)

    d.appendVarFlag('do_image', 'vardeps', ' '.join(vardeps))

    maskedtypes = (d.getVar('IMAGE_TYPES_MASKED') or "").split()
    maskedtypes = [dbg + t for t in maskedtypes for dbg in ("", "debugfs_")]

    for t in basetypes:
        vardeps = set()
        cmds = []
        subimages = []
        realt = t

        if t in maskedtypes:
            continue

        localdata = bb.data.createCopy(d)
        debug = ""
        if t.startswith("debugfs_"):
            setup_debugfs_variables(localdata)
            debug = "setup_debugfs "
            realt = t[8:]
        localdata.setVar('OVERRIDES', '%s:%s' % (realt, old_overrides))
        bb.data.update_data(localdata)
        localdata.setVar('type', realt)
        # Delete DATETIME so we don't expand any references to it now
        # This means the task's hash can be stable rather than having hardcoded
        # date/time values. It will get expanded at execution time.
        # Similarly TMPDIR since otherwise we see QA stamp comparision problems
        localdata.delVar('DATETIME')
        localdata.delVar('TMPDIR')

        image_cmd = localdata.getVar("IMAGE_CMD")
        vardeps.add('IMAGE_CMD_' + realt)
        if image_cmd:
            cmds.append("\t" + image_cmd)
        else:
            bb.fatal("No IMAGE_CMD defined for IMAGE_FSTYPES entry '%s' - possibly invalid type name or missing support class" % t)
        cmds.append(localdata.expand("\tcd ${IMGDEPLOYDIR}"))

        # Since a copy of IMAGE_CMD_xxx will be inlined within do_image_xxx,
        # prevent a redundant copy of IMAGE_CMD_xxx being emitted as a function.
        d.delVarFlag('IMAGE_CMD_' + realt, 'func')

        rm_tmp_images = set()
        def gen_conversion_cmds(bt):
            for ctype in ctypes:
                if bt[bt.find('.') + 1:] == ctype:
                    type = bt[0:-len(ctype) - 1]
                    if type.startswith("debugfs_"):
                        type = type[8:]
                    # Create input image first.
                    gen_conversion_cmds(type)
                    localdata.setVar('type', type)
                    cmd = "\t" + (localdata.getVar("CONVERSION_CMD_" + ctype) or localdata.getVar("COMPRESS_CMD_" + ctype))
                    if cmd not in cmds:
                        cmds.append(cmd)
                    vardeps.add('CONVERSION_CMD_' + ctype)
                    vardeps.add('COMPRESS_CMD_' + ctype)
                    subimage = type + "." + ctype
                    if subimage not in subimages:
                        subimages.append(subimage)
                    if type not in alltypes:
                        rm_tmp_images.add(localdata.expand("${IMAGE_NAME}${IMAGE_NAME_SUFFIX}.${type}"))

        for bt in basetypes[t]:
            gen_conversion_cmds(bt)

        localdata.setVar('type', realt)
        if t not in alltypes:
            rm_tmp_images.add(localdata.expand("${IMAGE_NAME}${IMAGE_NAME_SUFFIX}.${type}"))
        else:
            subimages.append(realt)

        # Clean up after applying all conversion commands. Some of them might
        # use the same input, therefore we cannot delete sooner without applying
        # some complex dependency analysis.
        for image in rm_tmp_images:
            cmds.append("\trm " + image)

        after = 'do_image'
        for dep in typedeps[t]:
            after += ' do_image_%s' % dep.replace("-", "_").replace(".", "_")

        t = t.replace("-", "_").replace(".", "_")

        d.setVar('do_image_%s' % t, '\n'.join(cmds))
        d.setVarFlag('do_image_%s' % t, 'func', '1')
        d.setVarFlag('do_image_%s' % t, 'fakeroot', '1')
        d.setVarFlag('do_image_%s' % t, 'prefuncs', debug + 'set_image_size')
        d.setVarFlag('do_image_%s' % t, 'postfuncs', 'create_symlinks')
        d.setVarFlag('do_image_%s' % t, 'subimages', ' '.join(subimages))
        d.appendVarFlag('do_image_%s' % t, 'vardeps', ' '.join(vardeps))
        d.appendVarFlag('do_image_%s' % t, 'vardepsexclude', 'DATETIME')

        bb.debug(2, "Adding type %s before %s, after %s" % (t, 'do_image_complete', after))
        bb.build.addtask('do_image_%s' % t, 'do_image_complete', after, d)
}

#
# Compute the rootfs size
#
def get_rootfs_size(d):
    import subprocess

    rootfs_alignment = int(d.getVar('IMAGE_ROOTFS_ALIGNMENT'))
    overhead_factor = float(d.getVar('IMAGE_OVERHEAD_FACTOR'))
    rootfs_req_size = int(d.getVar('IMAGE_ROOTFS_SIZE'))
    rootfs_extra_space = eval(d.getVar('IMAGE_ROOTFS_EXTRA_SPACE'))
    rootfs_maxsize = d.getVar('IMAGE_ROOTFS_MAXSIZE')
    image_fstypes = d.getVar('IMAGE_FSTYPES') or ''
    initramfs_fstypes = d.getVar('INITRAMFS_FSTYPES') or ''
    initramfs_maxsize = d.getVar('INITRAMFS_MAXSIZE')

    output = subprocess.check_output(['du', '-ks',
                                      d.getVar('IMAGE_ROOTFS')])
    size_kb = int(output.split()[0])
    base_size = size_kb * overhead_factor
    base_size = max(base_size, rootfs_req_size) + rootfs_extra_space

    if base_size != int(base_size):
        base_size = int(base_size + 1)
    else:
        base_size = int(base_size)

    base_size += rootfs_alignment - 1
    base_size -= base_size % rootfs_alignment

    # Do not check image size of the debugfs image. This is not supposed
    # to be deployed, etc. so it doesn't make sense to limit the size
    # of the debug.
    if (d.getVar('IMAGE_BUILDING_DEBUGFS') or "") == "true":
        return base_size

    # Check the rootfs size against IMAGE_ROOTFS_MAXSIZE (if set)
    if rootfs_maxsize:
        rootfs_maxsize_int = int(rootfs_maxsize)
        if base_size > rootfs_maxsize_int:
            bb.fatal("The rootfs size %d(K) overrides IMAGE_ROOTFS_MAXSIZE: %d(K)" % \
                (base_size, rootfs_maxsize_int))

    # Check the initramfs size against INITRAMFS_MAXSIZE (if set)
    if image_fstypes == initramfs_fstypes != ''  and initramfs_maxsize:
        initramfs_maxsize_int = int(initramfs_maxsize)
        if base_size > initramfs_maxsize_int:
            bb.error("The initramfs size %d(K) overrides INITRAMFS_MAXSIZE: %d(K)" % \
                (base_size, initramfs_maxsize_int))
            bb.error("You can set INITRAMFS_MAXSIZE a larger value. Usually, it should")
            bb.fatal("be less than 1/2 of ram size, or you may fail to boot it.\n")
    return base_size

python set_image_size () {
        rootfs_size = get_rootfs_size(d)
        d.setVar('ROOTFS_SIZE', str(rootfs_size))
        d.setVarFlag('ROOTFS_SIZE', 'export', '1')
}

#
# Create symlinks to the newly created image
#
python create_symlinks() {

    deploy_dir = d.getVar('IMGDEPLOYDIR')
    img_name = d.getVar('IMAGE_NAME')
    link_name = d.getVar('IMAGE_LINK_NAME')
    manifest_name = d.getVar('IMAGE_MANIFEST')
    taskname = d.getVar("BB_CURRENTTASK")
    subimages = (d.getVarFlag("do_" + taskname, 'subimages', False) or "").split()
    imgsuffix = d.getVarFlag("do_" + taskname, 'imgsuffix') or d.expand("${IMAGE_NAME_SUFFIX}.")

    if not link_name:
        return
    for type in subimages:
        dst = os.path.join(deploy_dir, link_name + "." + type)
        src = img_name + imgsuffix + type
        if os.path.exists(os.path.join(deploy_dir, src)):
            bb.note("Creating symlink: %s -> %s" % (dst, src))
            if os.path.islink(dst):
                os.remove(dst)
            os.symlink(src, dst)
        else:
            bb.note("Skipping symlink, source does not exist: %s -> %s" % (dst, src))
}

MULTILIBRE_ALLOW_REP =. "${base_bindir}|${base_sbindir}|${bindir}|${sbindir}|${libexecdir}|${sysconfdir}|${nonarch_base_libdir}/udev|/lib/modules/[^/]*/modules.*|"
MULTILIB_CHECK_FILE = "${WORKDIR}/multilib_check.py"
MULTILIB_TEMP_ROOTFS = "${WORKDIR}/multilib"

do_fetch[noexec] = "1"
do_unpack[noexec] = "1"
do_patch[noexec] = "1"
do_configure[noexec] = "1"
do_compile[noexec] = "1"
do_install[noexec] = "1"
do_populate_sysroot[noexec] = "1"
do_package[noexec] = "1"
do_package_qa[noexec] = "1"
do_packagedata[noexec] = "1"
do_package_write_ipk[noexec] = "1"
do_package_write_deb[noexec] = "1"
do_package_write_rpm[noexec] = "1"

# Allow the kernel to be repacked with the initramfs and boot image file as a single file
do_bundle_initramfs[depends] += "virtual/kernel:do_bundle_initramfs"
do_bundle_initramfs[nostamp] = "1"
do_bundle_initramfs[noexec] = "1"
do_bundle_initramfs () {
	:
}
addtask bundle_initramfs after do_image_complete

python extend_recipe_sysroot2() {
    import copy
    import subprocess

    taskdepdata = d.getVar("BB_TASKDEPDATA", False)
    mytaskname = d.getVar("BB_RUNTASK")
    #bb.warn(str(taskdepdata))
    pn = d.getVar("PN")

    if mytaskname.endswith("_setscene"):
        mytaskname = mytaskname.replace("_setscene", "")

    start = None
    configuredeps = []
    for dep in taskdepdata:
        data = taskdepdata[dep]
        if data[1] == mytaskname and data[0] == pn:
            start = dep
            break
    if start is None:
        bb.fatal("Couldn't find ourself in BB_TASKDEPDATA?")

    # We need to figure out which sysroot files we need to expose to this task.
    # This needs to match what would get restored from sstate, which is controlled 
    # ultimately by calls from bitbake to setscene_depvalid().
    # That function expects a setscene dependency tree. We build a dependency tree 
    # condensed to inter-sstate task dependencies, similar to that used by setscene 
    # tasks. We can then call into setscene_depvalid() and decide
    # which dependencies we can "see" and should expose in the recipe specific sysroot.
    setscenedeps = copy.deepcopy(taskdepdata)

    start = set([start])

    sstatetasks = d.getVar("SSTATETASKS").split()

    def print_dep_tree(deptree):
        data = ""
        for dep in deptree:
            deps = "    " + "\n    ".join(deptree[dep][3]) + "\n"
            data = "%s:\n  %s\n  %s\n%s  %s\n  %s\n" % (deptree[dep][0], deptree[dep][1], deptree[dep][2], deps, deptree[dep][4], deptree[dep][5])
        return data

    #bb.warn("Full dep tree is:\n%s" % print_dep_tree(taskdepdata))

    #bb.note(" start2 is %s" % str(start))

    # If start is an sstate task (like do_package) we need to add in its direct dependencies
    # else the code below won't recurse into them.
    for dep in set(start):
        for dep2 in setscenedeps[dep][3]:
            start.add(dep2)
        start.remove(dep)

    #bb.note(" start3 is %s" % str(start))

    # Create collapsed do_populate_sysroot -> do_populate_sysroot tree
    for dep in taskdepdata:
        data = setscenedeps[dep]        
        if data[1] not in sstatetasks:
            for dep2 in setscenedeps:
                data2 = setscenedeps[dep2]
                if dep in data2[3]:
                    data2[3].update(setscenedeps[dep][3])
                    data2[3].remove(dep)
            if dep in start:
                start.update(setscenedeps[dep][3])
                start.remove(dep)
            del setscenedeps[dep]

    # Remove circular references
    for dep in setscenedeps:
        if dep in setscenedeps[dep][3]:
            setscenedeps[dep][3].remove(dep)

    #bb.note("Computed dep tree is:\n%s" % print_dep_tree(setscenedeps))
    #bb.note(" start is %s" % str(start))
    #bb.warn("Computed dep tree is:\n%s" % str(setscenedeps))

    # Direct dependencies should be present and can be depended upon
    for dep in set(start):
        if setscenedeps[dep][1] == "do_populate_sysroot":
            if dep not in configuredeps:
                configuredeps.append(dep)
    #bb.note("Direct dependencies are %s" % str(configuredeps))
    #bb.note(" or %s" % str(start))

    # Call into setscene_depvalid for each sub-dependency and only copy sysroot files
    # for ones that would be restored from sstate.
    done = list(start)
    next = list(start)
    while next:
        new = []
        for dep in next:
            bb.note("Processing %s" % dep)
            data = setscenedeps[dep]
            for datadep in data[3]:
                bb.note("Processing dep %s" % datadep)
                if datadep in done:
                    continue
                taskdeps = {}
                taskdeps[dep] = setscenedeps[dep][:2]
                taskdeps[datadep] = setscenedeps[datadep][:2]
                retval = setscene_depvalid2(datadep, taskdeps, [], d)
                if retval:
                    bb.note("Skipping setscene dependency %s for installation into the sysroot" % datadep)
                    continue
                done.append(datadep)
                new.append(datadep)
                if datadep not in configuredeps and setscenedeps[datadep][1] == "do_populate_sysroot":
                    configuredeps.append(datadep)
                    bb.note("Adding dependency on %s" % setscenedeps[datadep][0])
                else:
                    bb.note("Following dependency on %s" % setscenedeps[datadep][0])
        next = new

    stagingdir = d.getVar("STAGING_DIR")
    recipesysroot = d.getVar("RECIPE_SYSROOT")
    recipesysrootnative = d.getVar("RECIPE_SYSROOT_NATIVE")

    # Detect bitbake -b usage
    nodeps = d.getVar("BB_LIMITEDDEPS") or False
    if nodeps:
        lock = bb.utils.lockfile(recipesysroot + "/sysroot.lock")
        staging_populate_sysroot_dir(recipesysroot, recipesysrootnative, True, d)
        staging_populate_sysroot_dir(recipesysroot, recipesysrootnative, False, d)
        bb.utils.unlockfile(lock)

    depdir = recipesysroot + "/installeddeps"
    bb.utils.mkdirhier(depdir)

    lock = bb.utils.lockfile(recipesysroot + "/sysroot.lock")

    fixme = []
    fixmenative = []
    postinsts = []

    for dep in configuredeps:
        c = setscenedeps[dep][0]
        taskhash = setscenedeps[dep][5]
        taskmanifest = depdir + "/" + c + "." + taskhash
        if mytaskname in ["do_sdk_depends", "do_populate_sdk_ext"] and c.endswith("-initial"):
            bb.note("Skipping initial setscene dependency %s for installation into the sysroot" % c)
            continue
        if os.path.exists(depdir + "/" + c):
            lnk = os.readlink(depdir + "/" + c)
            if lnk == c + "." + taskhash and os.path.exists(depdir + "/" + c + ".complete"): 
                bb.note("%s exists in sysroot, skipping" % c)
                continue
            else:
                bb.note("%s exists in sysroot, but is stale (%s vs. %s), removing." % (c, lnk, c + "." + taskhash))
                sstate_clean_manifest(depdir + "/" + lnk, d)
                os.unlink(depdir + "/" + c)
        elif os.path.lexists(depdir + "/" + c):
            os.unlink(depdir + "/" + c)

        os.symlink(c + "." + taskhash, depdir + "/" + c)

        native = False
        if c.endswith("-native"):
            manifest = d.expand("${SSTATE_MANIFESTS}/manifest-${BUILD_ARCH}-%s.populate_sysroot" % c)
            native = True
        elif c.startswith("nativesdk-"):
            manifest = d.expand("${SSTATE_MANIFESTS}/manifest-${SDK_ARCH}_${SDK_OS}-%s.populate_sysroot" % c)
        elif "-cross-" in c:
            manifest = d.expand("${SSTATE_MANIFESTS}/manifest-${BUILD_ARCH}_${TARGET_ARCH}-%s.populate_sysroot" % c)
            native = True
        elif "-crosssdk" in c:
            manifest = d.expand("${SSTATE_MANIFESTS}/manifest-${BUILD_ARCH}_${SDK_ARCH}_${SDK_OS}-%s.populate_sysroot" % c)
            native = True
        else:
            manifest = d.expand("${SSTATE_MANIFESTS}/manifest-${MACHINE_ARCH}-%s.populate_sysroot" % c)
            if not os.path.exists(manifest):
                manifest = d.expand("${SSTATE_MANIFESTS}/manifest-${TUNE_PKGARCH}-%s.populate_sysroot" % c)
            if not os.path.exists(manifest):
                manifest = d.expand("${SSTATE_MANIFESTS}/manifest-allarch-%s.populate_sysroot" % c)
        #if not os.path.exists(manifest):
        bb.warn("Looked for Manifest %s?" % manifest)

    #staging_processfixme(fixme, recipesysroot, recipesysroot, recipesysrootnative, d)
    #staging_processfixme(fixmenative, recipesysrootnative, recipesysroot, recipesysrootnative, d)

    #for p in postinsts:
    #    subprocess.check_call(p, shell=True)

    #for dep in configuredeps:
    #    c = setscenedeps[dep][0]
    #    open(depdir + "/" + c + ".complete", "w").close()

    bb.utils.unlockfile(lock)
}
extend_recipe_sysroot2[vardepsexclude] += "MACHINE SDK_ARCH BUILD_ARCH SDK_OS BB_TASKDEPDATA"

#python () {
#    d.appendVarFlag("do_rootfs", "prefuncs", " extend_recipe_sysroot2")
#}


def setscene_depvalid2(task, taskdependees, notneeded, d):
    # taskdependees is a dict of tasks which depend on task, each being a 3 item list of [PN, TASKNAME, FILENAME]
    # task is included in taskdependees too
    # Return - False - We need this dependency
    #        - True - We can skip this dependency

    bb.debug(2, "Considering setscene task: %s" % (str(taskdependees[task])))

    def isNativeCross(x):
        return x.endswith("-native") or "-cross-" in x or "-crosssdk" in x or x.endswith("-cross")

    def isPostInstDep(x):
        if x in ["qemu-native", "gdk-pixbuf-native", "qemuwrapper-cross", "depmodwrapper-cross", "systemd-systemctl-native", "gtk-icon-utils-native", "ca-certificates-native",
                 "glib-2.0-native", "kmod-native", "shadow-native"]:
            return True
        return False

    # We only need to trigger populate_lic through direct dependencies
    if taskdependees[task][1] == "do_populate_lic":
        return True

    # We only need to trigger packagedata through direct dependencies
    # but need to preserve packagedata on packagedata links
    if taskdependees[task][1] == "do_packagedata":
        for dep in taskdependees:
            if taskdependees[dep][1] == "do_packagedata":
                return False
        return True

    for dep in taskdependees:
        bb.debug(2, "  considering dependency: %s" % (str(taskdependees[dep])))
        if task == dep:
            continue
        if dep in notneeded:
            continue
        # do_package_write_* and do_package doesn't need do_package
        if taskdependees[task][1] == "do_package" and taskdependees[dep][1] in ['do_package', 'do_package_write_deb', 'do_package_write_ipk', 'do_package_write_rpm', 'do_packagedata', 'do_package_qa']:
            continue
        # do_package_write_* need do_populate_sysroot as they're mainly postinstall dependencies
        if taskdependees[task][1] == "do_populate_sysroot" and taskdependees[dep][1] in ['do_package_write_deb', 'do_package_write_ipk', 'do_package_write_rpm']:
            return False
        # do_package/packagedata/package_qa don't need do_populate_sysroot
        if taskdependees[task][1] == "do_populate_sysroot" and taskdependees[dep][1] in ['do_package', 'do_packagedata', 'do_package_qa']:
            continue
        # Native/Cross packages don't exist and are noexec anyway
        if isNativeCross(taskdependees[dep][0]) and taskdependees[dep][1] in ['do_package_write_deb', 'do_package_write_ipk', 'do_package_write_rpm', 'do_packagedata', 'do_package', 'do_package_qa']:
            continue

        # This is due to the [depends] in useradd.bbclass complicating matters
        # The logic *is* reversed here due to the way hard setscene dependencies are injected
        if (taskdependees[task][1] == 'do_package' or taskdependees[task][1] == 'do_populate_sysroot') and taskdependees[dep][0].endswith(('shadow-native', 'shadow-sysroot', 'base-passwd', 'pseudo-native')) and taskdependees[dep][1] == 'do_populate_sysroot':
            continue

        # Consider sysroot depending on sysroot tasks
        if taskdependees[task][1] == 'do_populate_sysroot' and taskdependees[dep][1] == 'do_populate_sysroot':
            # base-passwd/shadow-sysroot don't need their dependencies
            if taskdependees[dep][0].endswith(("base-passwd", "shadow-sysroot")):
                continue
            # Nothing need depend on libc-initial/gcc-cross-initial
            if "-initial" in taskdependees[task][0]:
                continue
            # For meta-extsdk-toolchain we want all sysroot dependencies
            if taskdependees[dep][0] == 'meta-extsdk-toolchain':
                return False
            # Native/Cross populate_sysroot need their dependencies
            if isNativeCross(taskdependees[task][0]) and isNativeCross(taskdependees[dep][0]):
                return False
            # Target populate_sysroot depended on by cross tools need to be installed
            if isNativeCross(taskdependees[dep][0]):
                return False
            # Native/cross tools depended upon by target sysroot are not needed
            if isNativeCross(taskdependees[task][0]):
                continue
            # Target populate_sysroot need their dependencies
            return False

        if taskdependees[task][1] == 'do_shared_workdir':
            continue

        if taskdependees[dep][1] == "do_populate_lic":
            continue


        # Safe fallthrough default
        bb.debug(2, " Default setscene dependency fall through due to dependency: %s" % (str(taskdependees[dep])))
        return False
    return True


