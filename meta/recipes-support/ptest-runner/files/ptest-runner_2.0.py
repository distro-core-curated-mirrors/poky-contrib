#!/usr/bin/env python

# Ptest-runner
#
# Copyright (C) 2014-2015 Intel Corporation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import sys
import fcntl
import time

import argparse
import logging 
from datetime import datetime

import subprocess

DEFAULT_LIBDIR='/usr/lib'
DEFAULT_TIMEOUT_SECS = 300

logging.basicConfig(format="%(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_available_ptests(libdir):
    ptests = {}

    if os.path.exists(libdir) and os.path.isdir(libdir):
        for d in os.listdir(libdir):
            full_d = os.path.join(libdir, d)
            if os.path.isdir(full_d) and not os.path.islink(full_d):
                run_ptest = os.path.join(full_d, 'ptest', 'run-ptest')
                if os.path.exists(run_ptest):
                    ptests[d] = run_ptest

    return ptests

def print_ptests(ptests):
    if ptests.keys():
        logger.info("Available ptests:\n")
        for p in ptests.keys():
            logger.info("%s\t%s" % (p, ptests[p]))
        return 0
    else:
        logger.error("No ptests found.\n")
        return 1

def get_ptests_to_run(available_ptests, requested_ptests):
    if requested_ptests:
        for rp in requested_ptests:
            if not rp in available_ptests.keys():
                logger.error("%s ptest isn't available." % rp)
                return 1

        for ap in available_ptests.keys():
            if not ap in requested_ptests:
                del available_ptests[ap]
    return 0

def run_ptests(ptests, timeout):
    def _set_nonblocking(fp):
        fd = process.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def _write_output(stdout):
        import select
        data_written = False

        rlist = [stdout.fileno()]
        (rrlist, _, _) = select.select(rlist, [], [], 0)

        for fd in rrlist:
            try:
                sys.stdout.write(stdout.read())
                data_written = True
            except:
                pass

        return data_written

    exit_code = 0

    print "START: %s" % sys.argv[0]
    for p in ptests.keys():
        run_ptest = ptests[p]

        print datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M")
        print "BEGIN: %s" % run_ptest

        os.chdir(os.path.dirname(run_ptest))

        process = subprocess.Popen([run_ptest], stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, shell=True, close_fds=True,
                bufsize=-1)
        _set_nonblocking(process.stdout)

        sentinel = datetime.now()
        while True:
            if _write_output(process.stdout):
                sentinel = datetime.now()
            elif timeout >= 0 and \
                ((datetime.now() - sentinel).total_seconds() > timeout):
                    print "\nTIMEOUT: %s" % run_ptest
                    process.kill()
                    break

            if process.poll() is not None:
                break

            time.sleep(0.5)

        if process.returncode:
            exit_code = process.returncode

        print "END: %s" % run_ptest
        print datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M")
    print "STOP: %s" % sys.argv[0]

    return exit_code

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ptest-runner runs ptests from upstream packages",
            add_help=False,
            epilog="Use %(prog)s [ptest1 ptest2 ...] --help to get help on a specific command")
    parser.add_argument('ptests', metavar='ptests', help='ptests to run',
            nargs='*')
    parser.add_argument('-d', '--directory', help='Directory for search ptests',
            action='store', default=DEFAULT_LIBDIR)
    parser.add_argument('-l', '--list', help='List available ptests',
            action='store_true')
    parser.add_argument('-t', '--timeout',
            help='Timeout (secs) for use when run ptests, -1 waits indefinitely', action='store', type=int,
            default=DEFAULT_TIMEOUT_SECS)
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='show this help message and exit')

    global_args, unparsed_args = parser.parse_known_args()

    ptests = get_available_ptests(global_args.directory)
    if global_args.list:
        exit_code = print_ptests(ptests)
        sys.exit(exit_code)

    exit_code = get_ptests_to_run(ptests, global_args.ptests)
    if exit_code:
        sys.exit(exit_code)

    sys.exit(run_ptests(ptests, global_args.timeout))
