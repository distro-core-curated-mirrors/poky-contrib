
BUILD_REPRODUCIBLE_BINARIES ??= "0"
BUILD_REPRODUCIBLE_BINARIES[export] = "1"

# Unix timestamp
REPRODUCIBLE_TIMESTAMP_ROOTFS ??= ""

def get_src_date_epoch_quick(d, path):
    import subprocess
    src_date_epoch = 0
    saved_cwd = os.getcwd()
    os.chdir(path)
    if path.endswith('/git'):
        src_date_epoch = int(subprocess.check_output(['git','log','-1','--pretty=%ct']))
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


def create_src_date_epoch_stamp(d):
    if d.getVar('BUILD_REPRODUCIBLE_BINARIES') == '1':
        path = d.getVar('S')

        #epochfile = os.path.join(path,'src_date_epoch.txt')
        #if os.path.isfile(epochfile):
        #    bb.warn(" *** path: %s reusing src_date_epoch.txt" % epochfile)
        #    return

        filename_dbg = None
        src_date_epoch = get_src_date_epoch_quick(d, path)

        if src_date_epoch == 0:
            exclude = set(["temp", "licenses", "patches", "recipe-sysroot-native", "recipe-sysroot", "pseudo"])
            for root, dirs, files in os.walk(path, topdown=True):
                files = [f for f in files if not f[0] == '.']
                dirs[:] = [d for d in dirs if not d[0] == '.']
                dirs[:] = [d for d in dirs if d not in exclude]
                if root.endswith('/git'):
                    bb.warn(" *** path: %s (git)" % path)
                    src_date_epoch = get_src_date_epoch_quick(d, root)
                    break

                for fname in files:
                    filename = os.path.join(root, fname)
                    try:
                        mtime = int(os.path.getmtime(filename))
                    except:
                        mtime = 0
                    if mtime > src_date_epoch:
                        src_date_epoch = mtime
                        filename_dbg = filename

        # Most likely an empty folder
        if src_date_epoch == 0:
            bb.warn("Unable to determine src_date_epoch! path:%s" % path)

        f = open(os.path.join(path,'src_date_epoch.txt'), 'w')
        f.write(str(src_date_epoch))
        f.close()

        if filename_dbg != None:
            bb.debug(1," src_date_epoch %d derived from: %s" % (src_date_epoch, filename_dbg))
            bb.warn(" src_date_epoch %d derived from: %s" % (src_date_epoch, filename_dbg))

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
        path = d.getVar('S')
        epochfile = os.path.join(path,'src_date_epoch.txt')
        if os.path.isfile(epochfile):
            f = open(epochfile, 'r')
            src_date_epoch = f.read()
            f.close()
            bb.debug(1, "src_date_epoch stamp found ---> stamp %s" % src_date_epoch)
            d.setVar('SOURCE_DATE_EPOCH', src_date_epoch)
        else:
            bb.debug(1, "src_date_epoch stamp not found.")
            d.setVar('SOURCE_DATE_EPOCH', '0')
    else:
        if 'PYTHONHASHSEED' in os.environ:
            del os.environ['PYTHONHASHSEED']
        if 'PERL_HASH_SEED' in os.environ:
            del os.environ['PERL_HASH_SEED']
        if 'SOURCE_DATE_EPOCH' in os.environ:
            del os.environ['SOURCE_DATE_EPOCH']
}
