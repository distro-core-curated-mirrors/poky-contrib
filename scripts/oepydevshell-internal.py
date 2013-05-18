#!/usr/bin/env python

import os
import sys
import time
import select
import fcntl

def nonblockingfd(fd):
    fcntl.fcntl(fd, fcntl.F_SETFL, fcntl.fcntl(fd, fcntl.F_GETFL) | os.O_NONBLOCK)

if len(sys.argv) != 2:
    print("Incorrect parameters")
    sys.exit(1)

try:
    print(sys.argv[1])
    pty = open(sys.argv[1], "w+b")
    nonblockingfd(pty)
    nonblockingfd(sys.stdin)
    while True:
        (ready, _, _) = select.select([pty, sys.stdin], [] , [], 1)
        if pty in ready:
            r = pty.read()
            sys.stdout.write(r)
        if sys.stdin in ready:
            r = sys.stdin.read()
            pty.write(r)
except Exception as e:
    print(str(e))
    time.sleep(5)

