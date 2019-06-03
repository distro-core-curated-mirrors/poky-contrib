# resulttool - common library/utility functions
#
# Copyright (c) 2019, Intel Corporation.
# Copyright (c) 2019, Linux Foundation
#
# SPDX-License-Identifier: GPL-2.0-only
#

import os
import base64
import zlib
import json
import scriptpath
import copy
import urllib.request
import posixpath
import datetime
import argparse
scriptpath.add_oe_lib_path()

flatten_map = {
    "oeselftest": [],
    "runtime": [],
    "sdk": [],
    "sdkext": [],
    "manual": []
}
regression_map = {
    "oeselftest": ['TEST_TYPE', 'MACHINE'],
    "runtime": ['TESTSERIES', 'TEST_TYPE', 'IMAGE_BASENAME', 'MACHINE', 'IMAGE_PKGTYPE', 'DISTRO'],
    "sdk": ['TESTSERIES', 'TEST_TYPE', 'IMAGE_BASENAME', 'MACHINE', 'SDKMACHINE'],
    "sdkext": ['TESTSERIES', 'TEST_TYPE', 'IMAGE_BASENAME', 'MACHINE', 'SDKMACHINE'],
    "manual": ['TEST_TYPE', 'TEST_MODULE', 'IMAGE_BASENAME', 'MACHINE']
}
store_map = {
    "oeselftest": ['TEST_TYPE'],
    "runtime": ['TEST_TYPE', 'DISTRO', 'MACHINE', 'IMAGE_BASENAME'],
    "sdk": ['TEST_TYPE', 'MACHINE', 'SDKMACHINE', 'IMAGE_BASENAME'],
    "sdkext": ['TEST_TYPE', 'MACHINE', 'SDKMACHINE', 'IMAGE_BASENAME'],
    "manual": ['TEST_TYPE', 'TEST_MODULE', 'MACHINE', 'IMAGE_BASENAME']
}

def is_url(p):
    """
    Helper for determining if the given path is a URL
    """
    return p.startswith('http://') or p.startswith('https://')

extra_configvars = {'TESTSERIES': ''}

#
# Load the json file and append the results data into the provided results dict
#
def append_resultsdata(results, f, configmap=store_map, configvars=extra_configvars):
    if type(f) is str:
        if is_url(f):
            with urllib.request.urlopen(f) as response:
                data = json.loads(response.read().decode('utf-8'))
            url = urllib.parse.urlparse(f)
            testseries = posixpath.basename(posixpath.dirname(url.path))
        else:
            with open(f, "r") as filedata:
                data = json.load(filedata)
            testseries = os.path.basename(os.path.dirname(f))
    else:
        data = f
    for res in data:
        if "configuration" not in data[res] or "result" not in data[res]:
            raise ValueError("Test results data without configuration or result section?")
        for config in configvars:
            if config == "TESTSERIES" and "TESTSERIES" not in data[res]["configuration"]:
                data[res]["configuration"]["TESTSERIES"] = testseries
                continue
            if config not in data[res]["configuration"]:
                data[res]["configuration"][config] = configvars[config]
        testtype = data[res]["configuration"].get("TEST_TYPE")
        if testtype not in configmap:
            raise ValueError("Unknown test type %s" % testtype)
        testpath = "/".join(data[res]["configuration"].get(i) for i in configmap[testtype])
        if testpath not in results:
            results[testpath] = {}
        results[testpath][res] = data[res]

#
# Walk a directory and find/load results data
# or load directly from a file
#
def load_resultsdata(source, configmap=store_map, configvars=extra_configvars):
    results = {}
    if is_url(source) or os.path.isfile(source):
        append_resultsdata(results, source, configmap, configvars)
        return results
    for root, dirs, files in os.walk(source):
        for name in files:
            f = os.path.join(root, name)
            if name == "testresults.json":
                append_resultsdata(results, f, configmap, configvars)
    return results

def filter_resultsdata(results, resultid):
    newresults = {}
    for r in results:
        for i in results[r]:
            if i == resultsid:
                 newresults[r] = {}
                 newresults[r][i] = results[r][i]
    return newresults

def strip_ptestresults(results):
    newresults = copy.deepcopy(results)
    #for a in newresults2:
    #  newresults = newresults2[a]
    for res in newresults:
        if 'result' not in newresults[res]:
            continue
        if 'ptestresult.rawlogs' in newresults[res]['result']:
            del newresults[res]['result']['ptestresult.rawlogs']
        if 'ptestresult.sections' in newresults[res]['result']:
            for i in newresults[res]['result']['ptestresult.sections']:
                if 'log' in newresults[res]['result']['ptestresult.sections'][i]:
                    del newresults[res]['result']['ptestresult.sections'][i]['log']
    return newresults

def decode_log(logdata):
    if isinstance(logdata, str):
        return logdata
    elif isinstance(logdata, dict):
        if "compressed" in logdata:
            data = logdata.get("compressed")
            data = base64.b64decode(data.encode("utf-8"))
            data = zlib.decompress(data)
            return data.decode("utf-8", errors='ignore')
    return None

def ptestresult_get_log(results, section):
    if 'ptestresult.sections' not in results:
        return None
    if section not in results['ptestresult.sections']:
        return None

    ptest = results['ptestresult.sections'][section]
    if 'log' not in ptest:
        return None
    return decode_log(ptest['log'])

def ptestresult_get_rawlogs(results):
    if 'ptestresult.rawlogs' not in results:
        return None
    if 'log' not in results['ptestresult.rawlogs']:
        return None
    return decode_log(results['ptestresult.rawlogs']['log'])

def save_resultsdata(results, destdir, fn="testresults.json", ptestjson=False, ptestlogs=False):
    for res in results:
        if res:
            dst = destdir + "/" + res + "/" + fn
        else:
            dst = destdir + "/" + fn
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        resultsout = results[res]
        if not ptestjson:
            resultsout = strip_ptestresults(results[res])
        with open(dst, 'w') as f:
            f.write(json.dumps(resultsout, sort_keys=True, indent=4))
        for res2 in results[res]:
            if ptestlogs and 'result' in results[res][res2]:
                seriesresults = results[res][res2]['result']
                rawlogs = ptestresult_get_rawlogs(seriesresults)
                if rawlogs is not None:
                    with open(dst.replace(fn, "ptest-raw.log"), "w+") as f:
                        f.write(rawlogs)
                if 'ptestresult.sections' in seriesresults:
                    for i in seriesresults['ptestresult.sections']:
                        sectionlog = ptestresult_get_log(seriesresults, i)
                        if sectionlog is not None:
                            with open(dst.replace(fn, "ptest-%s.log" % i), "w+") as f:
                                f.write(sectionlog)

def git_get_result(repo, tags, configmap=store_map):
    git_objs = []
    for tag in tags:
        files = repo.run_cmd(['ls-tree', "--name-only", "-r", tag]).splitlines()
        git_objs.extend([tag + ':' + f for f in files if f.endswith("testresults.json")])

    def parse_json_stream(data):
        """Parse multiple concatenated JSON objects"""
        objs = []
        json_d = ""
        for line in data.splitlines():
            if line == '}{':
                json_d += '}'
                objs.append(json.loads(json_d))
                json_d = '{'
            else:
                json_d += line
        objs.append(json.loads(json_d))
        return objs

    # Optimize by reading all data with one git command
    results = {}
    for obj in parse_json_stream(repo.run_cmd(['show'] + git_objs + ['--'])):
        append_resultsdata(results, obj, configmap=configmap)

    return results

class SliceAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs, **kwargs)

    def __call__(self, parser, namespace, value, options_string=None):
        s = [int(x) for x in value.split(':')]
        if len(s) < 1 or len(s) > 3:
            raise ValueError("'%s' is not a valid slice" % value)
        setattr(namespace, self.dest, s)

def add_run_slice_arg(parser, default=None):
    if default:
        default_help = ':'.join("%d" % d for d in default)
    else:
        default_help = 'all test runs'

    parser.add_argument('--run', help='''Filter out runs by timestamp. Uses
        Python list indexing and slice notation where 0 is the newest test
        run and -1 is the oldest. The default if unspecified is ''' + default_help,
        metavar='SLICE', action=SliceAction, default=default)

def test_run_results(results, run_slice=None):
    """
    Convenient generator function that iterates over all test runs that have a
    result section.

    Generates a tuple of:
        (result json file path, test run name, test run (dict), test run "results" (dict))
    for each test run that has a "result" section
    """
    def has_starttime(r):
        return 'configuration' in r and 'STARTTIME' in r['configuration']

    def get_starttime(r):
        return datetime.datetime.strptime(r["configuration"]["STARTTIME"], '%Y%m%d%H%M%S')

    test_runs = []
    for path in results:
        test_runs.extend((path, name, results[path][name]) for name in results[path].keys())

    if run_slice is not None:
        # Filter out any test runs without a starting time
        test_runs = [(path, name, run) for (path, name, run) in test_runs if has_starttime(run)]

        # Sort remaining test runs by date
        test_runs.sort(key=lambda x: get_starttime(x[2]), reverse=True)

        if len(run_slice) == 1:
            test_runs = [test_runs[run_slice[0]]]
        elif len(run_slice) == 2:
            test_runs = test_runs[run_slice[0]:run_slice[1]]
        elif len(run_slice) == 3:
            test_runs = test_runs[run_slice[0]:run_slice[1]:run_slice[2]]
        else:
            raise ValueError("Invalid slice '%r' specified" % run_slice)

    for path, run_name, run in test_runs:
        if not 'result' in run:
            continue

        yield path, run_name, run, run['result']

