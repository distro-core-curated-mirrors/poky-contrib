MINIFEED_DIR = "${WORKDIR}/minifeed"

addtask minifeed2 after do_build
# this seem to build target gcc??
#do_minifeed2[deptask] = "do_build"

python do_minifeed2() {
    taskname = ":do_package_write_"
    
    taskdepdata = d.getVar("BB_TASKDEPDATA", False)
    pn = d.getVar("PN")
    task = d.getVar("BB_RUNTASK")

    # Find our starting task
    start = None
    for dep in taskdepdata:
        data = taskdepdata[dep]
        if data[0] == pn and data[1] == task:
            start = dep
            break
    if start is None:
        bb.fatal(f"Could not find starting task {pn}:{task}")

    queue = [start]
    seen = set()
    pkgdeps = set()

    while queue:
        entry = taskdepdata[queue.pop()]
        #bb.warn(str(entry))
        deps = entry[3]
        for dep in deps:
            if dep in seen:
                continue
            seen.add(dep)
            queue.append(dep)

            if taskname in dep:
                pkgdeps.add(dep)

    bb.warn(str(pkgdeps))
}
