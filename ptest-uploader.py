#!/usr/bin/python
import os
import sys
import time
import subprocess
import re
from datetime import datetime, timedelta
import glob
from logparser import *
import shutil

def parse_ptest(logfile):
    parser = Lparser(test_0_pass_regex="^PASS:(.+)", test_0_fail_regex="^FAIL:(.+)", section_0_begin_regex="^BEGIN: .*/(.+)/ptest", section_0_end_regex="^END: .*/(.+)/ptest")
    parser.init()
    result = Result()

    with open(logfile) as f:
        for line in f:
            result_tuple = parser.parse_line(line)
            if not result_tuple:
                continue
            result_tuple = line_type, category, status, name = parser.parse_line(line)

            if line_type == 'section' and status == 'begin':
                current_section = name
                continue

            if line_type == 'section' and status == 'end':
                current_section = None
                continue

            if line_type == 'test' and status == 'pass':
                result.store(current_section, name, status)
                continue

            if line_type == 'test' and status == 'fail':
                result.store(current_section, name, status)
                continue

    result.sort_tests()
    return result

try:
    ptest_file = str(sys.argv[1])
    bundle_context = str(sys.argv[2])
    machine_name = str(sys.argv[3])
    bundle_commit = str(sys.argv[4])
    bundle_date = str(sys.argv[5])
    test_image_type = str(sys.argv[6])
except:
    print "Usage: ptest-uploader.py file version machine_name commit date image_type\nptest-uploader.py ptest.log 1.9 NUC f9ea480e6c26fea46c3011c4e9d0e2de3d5c81b4 2015-07-10 core-image-sato-sdk"
    exit(1)

print "Starting parsing ptest log..."

result = parse_ptest(ptest_file)
log_results_to_location = "./ptest-results"
if os.path.exists(log_results_to_location):
    shutil.rmtree(log_results_to_location)
os.makedirs(log_results_to_location)

result.log_as_files(log_results_to_location, test_status = ['pass','fail'])

print "Uploading ptest logs to lava..."
ptest_results = os.path.join(os.path.dirname(os.path.abspath(ptest_file)), "ptest-results")
for file in os.listdir(ptest_results):
    os.system("python ptest2bundle.py "+os.path.join(str(ptest_results),str(file))+" %s %s %s %s %s " % (bundle_context, machine_name, bundle_commit, bundle_date, test_image_type))
    print "Uploaded: %s" % str(file)
print "Removing loca bundle files..."
os.system("rm *.bundle")
print "All done."