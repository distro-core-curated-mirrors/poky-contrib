addtask throwerror
do_throwerror[nostamp] = "1"
python do_throwerror() {
    bb.warn("About to crash...")
    raise RuntimeError("argh!")
}

addtask spawnerror
do_spawnerror[nostamp] = "1"
python do_spawnerror() {
    import subprocess
    subprocess.check_output("echo about to fail; echo here we go; false", shell=True, stderr=subprocess.STDOUT)
}

addtask spawnerrorbinary
do_spawnerrorbinary[nostamp] = "1"
python do_spawnerrorbinary() {
    import subprocess
    subprocess.check_output("head -c 10 /bin/bash; false", shell=True, stderr=subprocess.STDOUT)
}

addtask emiterror
do_emiterror[nostamp] = "1"
python do_emiterror() {
    bb.warn("this is a warning")
    bb.error("this is an error")
    bb.error("this is an error\non two lines")
}

addtask shellerror
do_shellerror[nostamp] = "1"
do_shellerror() {
    bbwarn This is a warning
    bberror This is an error
    bbfatal This is fatal
    bbwarn This should not appear
}
