inherit terminal

DEVSHELL = "${SHELL}"

python do_devshell () {
    if d.getVarFlag("do_devshell", "manualfakeroot"):
       d.prependVar("DEVSHELL", "pseudo ")
       fakeenv = d.getVar("FAKEROOTENV", True).split()
       for f in fakeenv:
            k = f.split("=")
            d.setVar(k[0], k[1])           
            d.appendVar("OE_TERMINAL_EXPORTS", " " + k[0])
       d.delVarFlag("do_devshell", "fakeroot")

    oe_terminal(d.getVar('DEVSHELL', True), 'OpenEmbedded Developer Shell', d)
}

addtask devshell after do_patch

do_devshell[dirs] = "${S}"
do_devshell[nostamp] = "1"

# devshell and fakeroot/pseudo need careful handling since only the final
# command should run under fakeroot emulation, any X connection should
# be done as the normal user. We therfore carefully construct the envionment
# manually
python () {
    if d.getVarFlag("do_devshell", "fakeroot"):
       # We need to signal our code that we want fakeroot however we
       # can't manipulate the environment and variables here yet (see YOCTO #4795)
       d.setVarFlag("do_devshell", "manualfakeroot", "1")
       d.delVarFlag("do_devshell", "fakeroot")
} 

python do_devpyshell() {
    m, s = os.openpty()
    sname = os.ttyname(s)
    os.system('stty cs8 -icanon -echo < %s' % sname)
    pid = os.fork()
    if pid:
        oe_terminal("oepydevshell-internal.py %s" % sname, 'OpenEmbedded Developer PyShell', d)
        os._exit(0)
    else:
        os.dup2(m, sys.stdin.fileno())
        os.dup2(m, sys.stdout.fileno())
        os.dup2(m, sys.stderr.fileno())
        bb.utils.nonblockingfd(sys.stdout)
        bb.utils.nonblockingfd(sys.stdin)

        _context = {
            "os": os,
            "bb": bb,
            "time": time,
            "d": d,
        }

        import code
        try:
            code.interact("BB: ", local=_context)
        except Exception as e:
            bb.fatal(str(e))
}
addtask devpyshell after do_patch

do_devpyshell[nostamp] = "1"
