#!/usr/bin/python

import os
import sys
import time
import re
import subprocess


def run_ltp(milestone="M3", date="20150303"):
    print "Starting LTP tests..."
    default="syscalls\nfs\nfsx\ndio\nio\nmm\nipc\nsched\nmath\nnptl\npty\nadmin_tools\ntimers\ncommands"
    print "Writing configuration..."
    os.system("echo \""+default+"\" > /opt/ltp/scenario_groups/default")
    os.system("sed -e '/hackbench/ s/^#*/#/' -i /opt/ltp/runtest/sched")
    os.system("sed -e '/oom0/ s/^#*/#/' -i /opt/ltp/runtest/mm")
    print "Running test script..."
    os.system("cd /opt/ltp; ./runltp -p -l result-"+milestone+"-"+date+".log -C result-"+milestone+"-"+date+".fail -d /opt/ltp/tmp &> result-"+milestone+"-"+date+".fulllog")

def run_posix(milestone="M3", date="20150303"):
    print "Starting POSIX tests..."
    posix_sh="#!/bin/sh\n./bin/run-posix-option-group-test.sh AIO\n./bin/run-posix-option-group-test.sh MEM\n./bin/run-posix-option-group-test.sh MSG\n\
./bin/run-posix-option-group-test.sh SEM\n./bin/run-posix-option-group-test.sh SIG\n./bin/run-posix-option-group-test.sh THR\n./bin/run-posix-option-group-test.sh TMR\n\
./bin/run-posix-option-group-test.sh TPS"
    print "Running make..."
    os.system("cd /opt/ltp/testcases/open_posix_testsuite/; make generate-makefiles; make conformance-all; make conformance-test; make tools-all; make conformance-all;")
    os.system("echo \""+posix_sh+"\" > /opt/ltp/testcases/open_posix_testsuite/posix.sh")
    print "Running POSIX script..."
    os.system("cd /opt/ltp/testcases/open_posix_testsuite; sh posix.sh > posix.log")

def run_lsb(milestone="M3", date="20150303"):
    print "Starting LSB tests..."
    print "Setting up config files..."
    os.system("sed -i 's/which curl/which curl2/g' /usr/bin/LSB_Test.sh")
    os.system("sed -i 's/--quiet/--quiet --httpproxy proxy-jf.intel.com --httpport 911/g' /usr/bin/LSB_Test.sh")
    os.system("sed -i 's/lsb-qm-2.2.8./lsb-qm-2.2-12./' /opt/lsb-test/packages_list")
    print "Starting LSB script..."
    os.system("export http_proxy=http://proxy-jf.intel.com:911;export https_proxy=https://proxy-jf.intel.com:911; sh LSB_Test.sh")
    print "Configuration done. LSB script must be started from machine."

if __name__ == "__main__":
    milestone = sys.argv[1]
    date = sys.argv[2]
    run_ltp(milestone,date)
    run_posix(milestone,date)
    run_lsb(milestone,date)
