#!/usr/bin/env python


# Copyright (C) 2013 Intel Corporation
#
# Released under the MIT license (see COPYING.MIT)

# This script should be used outside of the build system to run image tests.
# It needs a json file as input as exported by the build.
# E.g for an already built image:
#- export the tests:
#   TEST_EXPORT_ONLY = "1"
#   TEST_TARGET  = "simpleremote"
#   TEST_TARGET_IP = "192.168.7.2"
#   TEST_SERVER_IP = "192.168.7.1"
# bitbake core-image-sato -c testimage
# Setup your target, e.g for qemu: runqemu core-image-sato
# cd build/tmp/testimage/core-image-sato
# ./runexported.py testdata.json

import sys
import os
import time
from optparse import OptionParser, make_option

try:
    import simplejson as json
except ImportError:
    import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "oeqa")))

from oeqa.base.targetrunner import TargetTestRunner, TestProgram
from oeqa.oetest import OETestRunner
from oeqa.utils.sshcontrol import SSHControl
from oeqa.base.controller.base_target import BaseTarget

# this isn't pretty but we need a fake target object
# for running the tests externally as we don't care
# about deploy/start we only care about the connection methods (run, copy)
class FakeTarget(BaseTarget):
    def __init__(self, d):
        self.connection = None
        self.ip = None
        self.server_ip = None
        self.datetime = time.strftime('%Y%m%d%H%M%S',time.gmtime())
        self.testdir = d.getVar("TEST_LOG_DIR", True)
        self.pn = d.getVar("PN", True)

    def start(self):
        super(FakeTarget, self).start()
        self.sshlog = os.path.join(self.testdir, "ssh_target_log.%s" % self.datetime)
        sshloglink = os.path.join(self.testdir, "ssh_target_log")
        if os.path.islink(sshloglink):
            os.unlink(sshloglink)
        os.symlink(self.sshlog, sshloglink)
        print("SSH log file: %s" %  self.sshlog)
        self.connection = SSHControl(self.ip, logfile=self.sshlog)

    def stop(self):
        return super(FakeTarget, self).stop()

class MyDataDict(dict):
    def getVar(self, key, unused = None):
        return self.get(key, "")

class TestProgramExport(TestProgram):
    runner_class = OETestRunner
    def options(self):
        super(TestProgramExport, self).options()
        self.option_list.extend([
            make_option("-t", "--target-ip", dest="ip", help="The IP address of the target machine. Use this to \
            overwrite the value determined from TEST_TARGET_IP at build time"),
            make_option("-s", "--server-ip", dest="server_ip", help="The IP address of this machine. Use this to \
            overwrite the value determined from TEST_SERVER_IP at build time."),
            make_option("-d", "--deploy-dir", dest="deploy_dir", help="Full path to the package feeds, that this \
            the contents of what used to be DEPLOY_DIR on the build machine. If not specified it will use the value \
            specified in the json if that directory actually exists or it will error out.")
        ])

    def configure(self, options=None):
        super(TestProgramExport, self).configure(options)
        options, args = options if isinstance(options, tuple) else (options, None)
        if not args:
            self.parser.error("Incorrect number of arguments. The one and only argument should be a json file exported by the build system")
        with open(args[0], "r") as f:
            loaded = json.load(f)
        if options.ip:
            loaded["target"]["ip"] = options.ip
        if options.server_ip:
            loaded["target"]["server_ip"] = options.server_ip

        d = MyDataDict()
        for key in loaded["d"].keys():
            d[key] = loaded["d"][key]

        if options.logdir:
            d["TEST_LOG_DIR"] = options.logdir
        else:
            d["TEST_LOG_DIR"] = os.path.abspath(os.path.dirname(__file__))
        if options.deploy_dir:
            d["DEPLOY_DIR"] = options.deploy_dir
        else:
            if not os.path.isdir(d["DEPLOY_DIR"]):
                raise Exception("The path to DEPLOY_DIR does not exists: %s" % d["DEPLOY_DIR"])

        target = FakeTarget(d)
        for key in loaded["target"].keys():
            setattr(target, key, loaded["target"][key])

        setattr(self.context, "d", d)
        setattr(self.context, "target", target)
        for key in loaded.keys():
            if key != "d" and key != "target":
                setattr(self.context, key, loaded[key])

main = TestProgramExport

if __name__ == "__main__":
    try:
        main()
    except Exception:
        ret = 1
        import traceback
        traceback.print_exc(5)
