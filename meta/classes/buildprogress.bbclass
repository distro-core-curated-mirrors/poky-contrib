BUILD_PROGRESS_THRESHOLD = "2"

def read_task_profile(d):
    if not d.getVar('BB_CURRENTTASK', False):
        return 0
    import errno
    profilefile = d.expand('${TMPDIR}/taskprofile/${PN}.do_${BB_CURRENTTASK}')
    #bb.warn('%s.%s: %s' % (d.getVar('PN', True),d.getVar('BB_CURRENTTASK', True), profilefile))
    linecount = 0
    try:
        with open(profilefile, 'r') as f:
            linecount = int(f.read())
        #bb.warn('%s.%s: %d' % (d.getVar('PN', True),d.getVar('BB_CURRENTTASK', True),linecount))
    except IOError as e:
        if e.errno != errno.ENOENT:
            raise
    return linecount


python() {
    tasks = filter(lambda k: d.getVarFlag(k, "task"), d.keys())
    for task in tasks:
        if task not in ['do_rootfs', 'do_fetch'] and not d.getVarFlag('progress', False):
            d.setVarFlag(task, 'progress', 'linecount:${@read_task_profile(d)}')
}


progress_profile_task() {
    import time

    taskfile = e.data.expand('${TMPDIR}/taskprofile/running/%s' % e.pid)

    rmtask = False

    if isinstance(e, bb.build.TaskStarted):
        bb.utils.mkdirhier(os.path.dirname(taskfile))
        with open(taskfile, 'w') as f:
            f.write('%f' % time.time())
    elif isinstance(e, bb.build.TaskSucceeded):
        with open(taskfile, 'r') as f:
            starttime = float(f.read())
        tasktime = time.time() - starttime
        if tasktime > float(d.getVar('BUILD_PROGRESS_THRESHOLD', True)):
            linecount = 0
            with open(e.logfile, 'r') as f:
                for line in f:
                    linecount += 1

            with open(e.data.expand('${TMPDIR}/taskprofile/${PN}.%s' % e.task), 'w') as f:
                f.write('%d' % linecount)
        rmtask = True
    elif isinstance(e, bb.build.TaskFailed):
        rmtask = True

    if rmtask:
        os.remove(taskfile)
}

addhandler progress_profile_task
progress_profile_task[eventmask] = "bb.build.TaskStarted bb.build.TaskSucceeded bb.build.TaskFailed"

