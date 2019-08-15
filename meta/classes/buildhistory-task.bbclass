SSTATEPOSTUNPACKFUNCS_append = " buildhistory_emit_outputsigs"
sstate_installpkgdir[vardepsexclude] += "buildhistory_emit_outputsigs"
SSTATEPOSTUNPACKFUNCS[vardepvalueexclude] .= "| buildhistory_emit_outputsigs"

python buildhistory_emit_outputsigs() {
    if not "task" in (d.getVar('BUILDHISTORY_FEATURES') or "").split():
        return

    import hashlib

    taskoutdir = os.path.join(d.getVar('BUILDHISTORY_DIR'), 'task', 'output')
    bb.utils.mkdirhier(taskoutdir)
    currenttask = d.getVar('BB_CURRENTTASK')
    pn = d.getVar('PN')
    taskfile = os.path.join(taskoutdir, '%s.%s' % (pn, currenttask))

    cwd = os.getcwd()
    filesigs = {}
    for root, _, files in os.walk(cwd):
        for fname in files:
            if fname == 'fixmepath':
                continue
            fullpath = os.path.join(root, fname)
            try:
                if os.path.islink(fullpath):
                    sha256 = hashlib.sha256(os.readlink(fullpath).encode('utf-8')).hexdigest()
                elif os.path.isfile(fullpath):
                    sha256 = bb.utils.sha256_file(fullpath)
                else:
                    continue
            except OSError:
                bb.warn('buildhistory: unable to read %s to get output signature' % fullpath)
                continue
            filesigs[os.path.relpath(fullpath, cwd)] = sha256
    with open(taskfile, 'w') as f:
        for fpath, fsig in sorted(filesigs.items(), key=lambda item: item[0]):
            f.write('%s %s\n' % (fpath, fsig))
}

python buildhistory_write_sigs() {
    if not "task" in (d.getVar('BUILDHISTORY_FEATURES') or "").split():
        return

    # Create sigs file
    if hasattr(bb.parse.siggen, 'dump_siglist'):
        taskoutdir = os.path.join(d.getVar('BUILDHISTORY_DIR'), 'task')
        bb.utils.mkdirhier(taskoutdir)
        bb.parse.siggen.dump_siglist(os.path.join(taskoutdir, 'tasksigs.txt'))
}

BUILDHISTORY_COMMIT_PREFUNCS += "buildhistory_write_sigs"
