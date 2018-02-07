
BUILD_REPRODUCIBLE_BINARIES ??= "1"
BUILD_REPRODUCIBLE_BINARIES[export] = "1"

# Unix timestamp
REPRODUCIBLE_TIMESTAMP_ROOTFS ??= ""

SDE_DIR ="${WORKDIR}/__sde__"
SDE_FILE = "${SDE_DIR}/__source_date_epoch.txt"

SSTATETASKS += "do_deploy_sde"

do_deploy_sde () {
    echo "Deploying SDE to ${SDE_DIR}."
}

python do_deploy_sde_setscene () {
    sstate_setscene(d)
}

do_deploy_sde[dirs] = "${SDE_DIR}"
do_deploy_sde[sstate-plaindirs] = "${SDE_DIR}"
addtask do_deploy_sde_setscene
addtask do_deploy_sde before do_configure after do_patch

def get_src_date_epoch_quick(d, path):
    import subprocess
    src_date_epoch = 0
    saved_cwd = os.getcwd()
    os.chdir(path)
    if os.path.isdir(".git"):
        try:
            src_date_epoch = int(subprocess.check_output(['git','log','-1','--pretty=%ct']))
        except subprocess.CalledProcessError as grepexc:
            bb.warn("Not a git repository in .git folder? error:%d" % (grepexc.returncode))
    else:
        known_files = set(["NEWS", "ChangeLog", "Changelog", "CHANGES"])

        for file in known_files:
            if os.path.isfile(file):
                mtime = int(os.path.getmtime(file))

                # There may be more than one "known_file" present.
                # If so, use the youngest one
                if mtime > src_date_epoch:
                    src_date_epoch = mtime

    os.chdir(saved_cwd)
    return src_date_epoch

python do_create_src_date_epoch_stamp() {
    if d.getVar('BUILD_REPRODUCIBLE_BINARIES') == '1':
        path = d.getVar('S')
        if not os.path.isdir(path):
            bb.warn("Unable to determine src_date_epoch! path:%s" % path)
            return
        epochfile = d.getVar('SDE_FILE')
        if os.path.isfile(epochfile):
            bb.debug(1, " path: %s reusing __source_date_epoch.txt" % epochfile)
            return

        # Expect cases such as S = "${WORKDIR}/git/xxx"
        gitpath = os.path.join(d.getVar('WORKDIR'),'git')
        if path.startswith(gitpath):
            path = gitpath

        filename_dbg = None
        src_date_epoch = get_src_date_epoch_quick(d, path)

        if src_date_epoch == 0:
            exclude = set(["temp", "licenses", "patches", "recipe-sysroot-native", "recipe-sysroot", "pseudo"])
            for root, dirs, files in os.walk(path, topdown=True):
                files = [f for f in files if not f[0] == '.']
                dirs[:] = [d for d in dirs if d not in exclude]

                for fname in files:
                    filename = os.path.join(root, fname)
                    try:
                        mtime = int(os.path.getmtime(filename))
                    except:
                        mtime = 0
                    if mtime > src_date_epoch:
                        src_date_epoch = mtime
                        filename_dbg = filename

        # Must be an empty folder...
        if src_date_epoch == 0:
            # kernel source do_unpack is special cased
            if not path.endswith("kernel-source"):
                bb.warn("Unable to determine src_date_epoch! path:%s" % path)

        bb.utils.mkdirhier(d.getVar('SDE_DIR'))
        f = open(epochfile, 'w')
        f.write(str(src_date_epoch))
        f.close()

        if filename_dbg != None:
            bb.debug(1," SOURCE_DATE_EPOCH %d derived from: %s" % (src_date_epoch, filename_dbg))
}

do_unpack[postfuncs] += "do_create_src_date_epoch_stamp"
#addtask do_create_src_date_epoch_stamp after do_unpack before do_patch

export PYTHONHASHSEED
export PERL_HASH_SEED
export SOURCE_DATE_EPOCH

BB_HASHBASE_WHITELIST += "SOURCE_DATE_EPOCH PYTHONHASHSEED PERL_HASH_SEED "

python () {
    import string, re

    # Create reproducible_environment

    if d.getVar('BUILD_REPRODUCIBLE_BINARIES') == '1':
        import subprocess
        d.setVar('PYTHONHASHSEED', '0')
        d.setVar('PERL_HASH_SEED', '0')
        d.setVar('TZ', 'UTC')
        epochfile = d.getVar('SDE_FILE')
        if os.path.isfile(epochfile):
            f = open(epochfile, 'r')
            src_date_epoch = f.read()
            f.close()
            bb.debug(1, "source_date_epoch stamp found ---> stamp %s" % src_date_epoch)
            d.setVar('SOURCE_DATE_EPOCH', src_date_epoch)
        else:
            #bb.warn("source_date_epoch stamp not found (%s)." % epochfile)
            d.setVar('SOURCE_DATE_EPOCH', '0')
    else:
        if 'PYTHONHASHSEED' in os.environ:
            del os.environ['PYTHONHASHSEED']
        if 'PERL_HASH_SEED' in os.environ:
            del os.environ['PERL_HASH_SEED']
        if 'SOURCE_DATE_EPOCH' in os.environ:
            del os.environ['SOURCE_DATE_EPOCH']
}
