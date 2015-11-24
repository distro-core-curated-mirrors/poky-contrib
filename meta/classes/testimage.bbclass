# Copyright (C) 2013 Intel Corporation
#
# Released under the MIT license (see COPYING.MIT)


# testimage.bbclass enables testing of qemu images using python unittests.
# Most of the tests are commands run on target image over ssh.
# To use it add testimage to global inherit and call your target image with -c testimage
# You can try it out like this:
# - first build a qemu core-image-sato
# - add INHERIT += "testimage" in local.conf
# - then bitbake core-image-sato -c testimage. That will run a standard suite of tests.

# You can set (or append to) TEST_SUITES in local.conf to select the tests
# which you want to run for your target.
# The test names are the module names in meta/lib/oeqa/runtime.
# Each name in TEST_SUITES represents a required test for the image. (no skipping allowed)
# Appending "auto" means that it will try to run all tests that are suitable for the image (each test decides that on it's own).
# Note that order in TEST_SUITES is relevant: tests are run in an order such that
# tests mentioned in @skipUnlessPassed run before the tests that depend on them,
# but without such dependencies, tests run in the order in which they are listed
# in TEST_SUITES.
#
# A layer can add its own tests in lib/oeqa/runtime, provided it extends BBPATH as normal in its layer.conf.

# TEST_LOG_DIR contains a command ssh log and may contain infromation about what command is running, output and return codes and for qemu a boot log till login.
# Booting is handled by this class, and it's not a test in itself.
# TEST_QEMUBOOT_TIMEOUT can be used to set the maximum time in seconds the launch code will wait for the login prompt.

TEST_LOG_DIR ?= "${WORKDIR}/testimage"

TEST_EXPORT_DIR ?= "${TMPDIR}/testimage/${PN}"
TEST_EXPORT_ONLY ?= "0"

RPMTESTSUITE = "${@bb.utils.contains('IMAGE_PKGTYPE', 'rpm', 'smart rpm', '', d)}"
MINTESTSUITE = "ping"
NETTESTSUITE = "${MINTESTSUITE} ssh df date scp syslog"
DEVTESTSUITE = "gcc kernelmodule ldd"

DEFAULT_TEST_SUITES = "${MINTESTSUITE} auto"
DEFAULT_TEST_SUITES_pn-core-image-minimal = "${MINTESTSUITE}"
DEFAULT_TEST_SUITES_pn-core-image-minimal-dev = "${MINTESTSUITE}"
DEFAULT_TEST_SUITES_pn-core-image-full-cmdline = "${NETTESTSUITE} perl python logrotate"
DEFAULT_TEST_SUITES_pn-core-image-x11 = "${MINTESTSUITE}"
DEFAULT_TEST_SUITES_pn-core-image-lsb = "${NETTESTSUITE} pam parselogs ${RPMTESTSUITE}"
DEFAULT_TEST_SUITES_pn-core-image-sato = "${NETTESTSUITE} connman xorg parselogs ${RPMTESTSUITE} \
    ${@bb.utils.contains('IMAGE_PKGTYPE', 'rpm', 'python', '', d)}"
DEFAULT_TEST_SUITES_pn-core-image-sato-sdk = "${NETTESTSUITE} connman xorg perl python \
    ${DEVTESTSUITE} parselogs ${RPMTESTSUITE}"
DEFAULT_TEST_SUITES_pn-core-image-lsb-dev = "${NETTESTSUITE} pam perl python parselogs ${RPMTESTSUITE}"
DEFAULT_TEST_SUITES_pn-core-image-lsb-sdk = "${NETTESTSUITE} buildcvs buildiptables buildsudoku \
    connman ${DEVTESTSUITE} pam perl python parselogs ${RPMTESTSUITE}"
DEFAULT_TEST_SUITES_pn-meta-toolchain = "auto"

# aarch64 has no graphics
DEFAULT_TEST_SUITES_remove_aarch64 = "xorg"

#qemumips is too slow for buildsudoku
DEFAULT_TEST_SUITES_remove_qemumips = "buildsudoku"

TEST_SUITES ?= "${DEFAULT_TEST_SUITES}"

TEST_QEMUBOOT_TIMEOUT ?= "1000"
TEST_TARGET ?= "qemu"
TEST_TARGET_IP ?= ""
TEST_SERVER_IP ?= ""

TESTIMAGEDEPENDS = ""
TESTIMAGEDEPENDS_qemuall = "qemu-native:do_populate_sysroot qemu-helper-native:do_populate_sysroot"

TESTIMAGELOCK = "${TMPDIR}/testimage.lock"
TESTIMAGELOCK_qemuall = ""

TESTIMAGE_DUMP_DIR ?= "/tmp/oe-saved-tests/"

testimage_dump_target () {
    top -bn1
    ps
    free
    df
    # The next command will export the default gateway IP
    export DEFAULT_GATEWAY=$(ip route | awk '/default/ { print $3}')
    ping -c3 $DEFAULT_GATEWAY
    dmesg
    netstat -an
    ip address
    # Next command will dump logs from /var/log/
    find /var/log/ -type f 2>/dev/null -exec echo "====================" \; -exec echo {} \; -exec echo "====================" \; -exec cat {} \; -exec echo "" \;
}

testimage_dump_host () {
    top -bn1
    iostat -x -z -N -d -p ALL 20 2
    ps -ef
    free
    df
    memstat
    dmesg
    ip -s link
    netstat -an
}

python do_testimage() {
    testimage_main(d)
}
addtask testimage
do_testimage[nostamp] = "1"
do_testimage[depends] += "${TESTIMAGEDEPENDS}"
do_testimage[lockfiles] += "${TESTIMAGELOCK}"

def exportTests(d,tc):
    import json
    import shutil
    import pkgutil
    import re

    exportpath = d.getVar("TEST_EXPORT_DIR", True)

    savedata = {}
    savedata["d"] = {}
    savedata["target"] = {}
    savedata["host_dumper"] = {}
    for key in tc.__dict__:
        # special cases
        if key not in ['d', 'target', 'host_dumper', 'suite']:
            savedata[key] = getattr(tc, key)
    savedata["target"]["ip"] = tc.target.ip or d.getVar("TEST_TARGET_IP", True)
    savedata["target"]["server_ip"] = tc.target.server_ip or d.getVar("TEST_SERVER_IP", True)

    keys = [ key for key in d.keys() if not key.startswith("_") and not key.startswith("BB") \
            and not key.startswith("B_pn") and not key.startswith("do_") and not d.getVarFlag(key, "func", True)]
    for key in keys:
        try:
            savedata["d"][key] = d.getVar(key, True)
        except bb.data_smart.ExpansionError:
            # we don't care about those anyway
            pass

    savedata["host_dumper"]["parent_dir"] = tc.host_dumper.parent_dir
    savedata["host_dumper"]["cmds"] = tc.host_dumper.cmds

    json_file = os.path.join(exportpath, "testdata.json")
    with open(json_file, "w") as f:
            json.dump(savedata, f, skipkeys=True, indent=4, sort_keys=True)

    # Replace absolute path with relative in the file
    exclude_path = os.path.join(d.getVar("COREBASE", True),'meta','lib','oeqa')
    f1 = open(json_file,'r').read()
    f2 = open(json_file,'w')
    m = f1.replace(exclude_path,'oeqa')
    f2.write(m)
    f2.close()

    # now start copying files
    # we'll basically copy everything under meta/lib/oeqa, with these exceptions
    #  - oeqa/targetcontrol.py - not needed
    #  - oeqa/selftest - something else
    # That means:
    #   - all tests from oeqa/runtime defined in TEST_SUITES (including from other layers)
    #   - the contents of oeqa/utils and oeqa/runtime/files
    #   - oeqa/oetest.py and oeqa/runexport.py (this will get copied to exportpath not exportpath/oeqa)
    #   - __init__.py files
    bb.utils.mkdirhier(os.path.join(exportpath, "oeqa/runtime/files"))
    bb.utils.mkdirhier(os.path.join(exportpath, "oeqa/utils"))
    # copy test modules, this should cover tests in other layers too
    bbpath = d.getVar("BBPATH", True).split(':')
    for t in tc.testslist:
        isfolder = False
        if re.search("\w+\.\w+\.test_\S+", t):
            t = '.'.join(t.split('.')[:3])
        mod = pkgutil.get_loader(t)
        # More depth than usual?
        if (t.count('.') > 2):
            for p in bbpath:
                foldername = os.path.join(p, 'lib',  os.sep.join(t.split('.')).rsplit(os.sep, 1)[0])
                if os.path.isdir(foldername):
                    isfolder = True
                    target_folder = os.path.join(exportpath, "oeqa", "runtime", os.path.basename(foldername))
                    if not os.path.exists(target_folder):
                        shutil.copytree(foldername, target_folder)
        if not isfolder:
            shutil.copy2(mod.filename, os.path.join(exportpath, "oeqa/runtime"))
    # copy __init__.py files
    oeqadir = pkgutil.get_loader("oeqa").filename
    shutil.copy2(os.path.join(oeqadir, "__init__.py"), os.path.join(exportpath, "oeqa"))
    shutil.copy2(os.path.join(oeqadir, "runtime/__init__.py"), os.path.join(exportpath, "oeqa/runtime"))
    # copy oeqa/oetest.py and oeqa/runexported.py
    shutil.copy2(os.path.join(oeqadir, "oetest.py"), os.path.join(exportpath, "oeqa"))
    shutil.copy2(os.path.join(oeqadir, "runexported.py"), exportpath)
    # copy oeqa/utils/*.py
    for root, dirs, files in os.walk(os.path.join(oeqadir, "utils")):
        for f in files:
            if f.endswith(".py"):
                shutil.copy2(os.path.join(root, f), os.path.join(exportpath, "oeqa/utils"))
    # copy oeqa/runtime/files/*
    for root, dirs, files in os.walk(os.path.join(oeqadir, "runtime/files")):
        for f in files:
            shutil.copy2(os.path.join(root, f), os.path.join(exportpath, "oeqa/runtime/files"))

    #integrating binaries too
    # creting needed directory structure
    arch = te.get_dest_folder(d.getVar("TUNE_FEATURES", True), os.listdir(d.getVar("DEPLOY_DIR_RPM", True)))
    bb.utils.mkdirhier(os.path.join(exportpath,"tar_files"))
    bb.utils.mkdirhier(os.path.join(exportpath,"binaries", arch, "packaged_binaries"))
    bb.utils.mkdirhier(os.path.join(exportpath,"binaries", "native"))
    bb.utils.mkdirhier(os.path.join(exportpath,"binaries", arch, "extracted_binaries"))
    with open(os.path.join(exportpath,"binaries",arch, "mapping.cfg"), "a") as mapping_file:
        #prepare the needed info for the mapping file
        mapping_params = dict()
        mapping_params[d.getVar("MACHINE",True)] = (d.getVar("TARGET_SYS",True), d.getVar("TUNE_FEATURES",True))
        mapping_file.write(mapping_params.__str__())

    populate_binaries(d)

    # create the "runner" tar file, but before that erase them if created in a previous run
    [runner_tar, bin_tar, native_tar] = [os.path.join(exportpath,"tar_files", item) for item in ("runner_files.tar", "{}_binaries.tar".format(arch), "native_binaries.tar")]
    for item in os.listdir(exportpath): # create the runner tarball
        if item not in ('binaries','tar_files'):
            create_tar(runner_tar, os.path.join(exportpath,item), item.replace(exportpath, ""))
    #create the binaries tar file
    for item in os.listdir(os.path.join(exportpath, "binaries")):
        if re.search("native", item): # creating native binaries tarfile
            create_tar(os.path.join(exportpath,"tar_files", os.path.basename(native_tar)), os.path.join(exportpath,"binaries", "native"), os.path.join("binaries", item.replace(exportpath, "")))
        else: # creating target binaries tar file
            create_tar(os.path.join(exportpath,"tar_files",os.path.basename(bin_tar)), os.path.join(exportpath,"binaries", arch), os.path.join("binaries", item.replace(exportpath, "")))
    bb.plain("Exported tests to: %s" % exportpath)
    for item in os.listdir(exportpath):
        if item == "tar_files":
            bb.plain("Exported tarballs to: {}".format(exportpath + "/tar_files"))

def create_tar(tar_fl,file_to_add, a_name=None):
    import tarfile as tar
    with tar.open(tar_fl,"a") as tar_file:
        tar_file.add(file_to_add, arcname=a_name) 

def obtain_binaries(d, param):
    """
    this func. will extract binaries based on their version (if required)
    """
    import oeqa.utils.testexport as te
    te.process_binaries(d, param) # for native packages, this is not extracting binaries, but only copies them
                                  # for a local machine with poky on it the user should build native binaries

def read_test_files(file_pth):
    """
    The only way to read what binaries are to be included in the tarball file(s) is to search for each
    test file (.py) and see if the decorator TestNeedsBin is present. If yes, just extract the information
    from there. The lib/oeqa/runtime dir is taken as default to read files from. The result is a list 
    containing needed information like binary name, binary, version etc. in a string of values separated 
    by "_". This aproach was taken because it helps when TestNeedsBin contains multiple binaries and some
    are with identical name and different version or when same binary is needed both in extracted and 
    packaged mode. A dictionary would have eliminated the duplicate same key (in our case binary name) 
    fields.
    """
    import re
    bin_ver = list()
    f_to_list = list()
    #the actual reading part of the file:
    with open(file_pth, 'r') as fl:
        f_to_list = list(fl)
    def process_found_tuple(list_of_tuples):
        for params in eval("{}".format(list_of_tuples)): # in our case, value is a list of values
            ver = ""
            packaged = ""
            t = ""
            for item in eval("{}".format(params)):
                if re.match("[0-9]+\.",item):
                    ver = item
                elif item == "rpm":
                    packaged = "rpm"
                elif item == "native":
                    t = item
            bin_ver.append("{}_{}_{}_{}".format(params[0],ver,packaged,t))

    def search_for_tuples_of_params(i):
        read_tuple = ""
        ind = i
        if re.search('\(\(', f_to_list[ind]) and not f_to_list[ind].startswith("#"): # the line is sure to be a valid one, not a comment
            read_tuple += f_to_list[ind].strip()
            while True:
                if re.search('\)\)', read_tuple):
                    read_tuple = read_tuple.replace("@TestNeedsBin","")#read_tuple[read_tuple.find('((')+1:read_tuple.find('))')+1]
                    break
                else:
                    ind += 1
                    read_tuple += f_to_list[ind].strip()
            process_found_tuple(read_tuple)
            return ind
        return

    # parsing all found lists
    for index,line in enumerate(f_to_list): 
        line=line.strip()
        if re.search("@TestNeedsBin", line) and not line.startswith("#") and not (re.search('\(\(', line) or re.search('\)\)', line)):
            packaged = ""
            version = ""
            t = ""
            for index, value in enumerate(eval(line.replace("@TestNeedsBin", ""))):
                if index == 0:
                    bin_name = value
                elif index == 1 and re.match("[0-9]+\.",value):
                    version = value
                elif value == "rpm":
                    packaged = value
                elif value == "native":
                    t = value
            bin_ver.append("{}_{}_{}_{}".format(bin_name,version,packaged,t))
        elif re.search("@TestNeedsBin", line) and not line.startswith("#") and (re.search('\(\(', line) or re.search('\)\)', line)):
            search_for_tuples_of_params(index)

    return bin_ver

def populate_binaries(d):
    default_pth_to_files = os.path.join(d.getVar("COREBASE",True), "meta/lib/oeqa/runtime")
    pth_to_file = list()
    pth_to_file.append(default_pth_to_files)
    bin_with_version = list()
    bbpath = d.getVar("BBPATH", True).split(':')
    testlist = get_tests_list(d)
    for pth in bbpath:
        for item in testlist:
            test_file_pth = os.path.join(pth, "lib", item.replace(".", os.sep) + ".py")
            if os.path.exists(test_file_pth):
                bin_with_version.extend(read_test_files(test_file_pth))
    for item in set(bin_with_version):
        obtain_binaries(d,item)

def testimage_main(d):
    import unittest
    import os
    import oeqa.runtime
    import time
    import signal
    from oeqa.oetest import ImageTestContext
    from oeqa.targetcontrol import get_target_controller
    from oeqa.utils.dump import get_host_dumper

    pn = d.getVar("PN", True)
    export = oe.utils.conditional("TEST_EXPORT_ONLY", "1", True, False, d)
    bb.utils.mkdirhier(d.getVar("TEST_LOG_DIR", True))
    if export:
        bb.utils.remove(d.getVar("TEST_EXPORT_DIR", True), recurse=True)
        bb.utils.mkdirhier(d.getVar("TEST_EXPORT_DIR", True))

    # we need the host dumper in test context
    host_dumper = get_host_dumper(d)

    # the robot dance
    target = get_target_controller(d)

    # test context
    tc = ImageTestContext(d, target, host_dumper)

    # this is a dummy load of tests
    # we are doing that to find compile errors in the tests themselves
    # before booting the image
    try:
        tc.loadTests()
    except Exception as e:
        import traceback
        bb.fatal("Loading tests failed:\n%s" % traceback.format_exc())

    if export:
        signal.signal(signal.SIGTERM, tc.origsigtermhandler)
        tc.origsigtermhandler = None
        exportTests(d,tc)
    else:
        target.deploy()
        try:
            target.start()
            starttime = time.time()
            result = tc.runTests()
            stoptime = time.time()
            if result.wasSuccessful():
                bb.plain("%s - Ran %d test%s in %.3fs" % (pn, result.testsRun, result.testsRun != 1 and "s" or "", stoptime - starttime))
                msg = "%s - OK - All required tests passed" % pn
                skipped = len(result.skipped)
                if skipped:
                    msg += " (skipped=%d)" % skipped
                bb.plain(msg)
            else:
                raise bb.build.FuncFailed("%s - FAILED - check the task log and the ssh log" % pn )
        finally:
            signal.signal(signal.SIGTERM, tc.origsigtermhandler)
            target.stop()

testimage_main[vardepsexclude] =+ "BB_ORIGENV"

inherit testsdk
