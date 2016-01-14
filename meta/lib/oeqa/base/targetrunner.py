#!/usr/bin/env python
# Copyright (C) 2013 Intel Corporation
#
# Released under the MIT license (see COPYING.MIT)

# test runner which support run testing on target device

"""test runner for target device"""
import sys
from optparse import make_option
from baserunner import TestRunnerBase

class TargetTestRunner(TestRunnerBase):
    '''test runner which support target DUT access'''
    def __init__(self):
        super(TargetTestRunner, self).__init__()

    def _get_arg_val(self, dest_name, store_val=True):
        '''get arg value from testrunner args'''
        args = sys.argv
        for opt in self.option_list:
            if opt.dest == dest_name:
                arg_names = opt._short_opts + opt._long_opts
                break
        else:
            return None

        for cur_arg in arg_names:
            try:
                ind = args.index(cur_arg)
                return args[ind+1] if store_val else True
            except:
                pass
        return None

    def options(self):
        '''expand extra options'''
        super(TargetTestRunner, self).options()
        ext_opts = [
            make_option("-c", "--controller", dest="controller",
                    help="the target controller to bridge host and target")
        ]
        self.option_list.extend(ext_opts)
        if self._get_arg_val("controller") == "ssh":
            self.option_list.append(
                   make_option("-t", "--target-ip", dest="ip",
                       help="The IP address of the target machine."))

    def configure(self, options):
        '''configure before testing'''
        super(TargetTestRunner, self).configure(options)
        if options.controller:
            if options.controller.lower() == "ssh":
                from controller.SSHTarget import SshRemoteTarget
                ssh_target = SshRemoteTarget(ip=options.ip)
                self.context.target = ssh_target

    def runtest(self, suite):
        '''run test suite with target'''
        if self.context.target:
            self.context.target.start()
        try:
            super(TargetTestRunner, self).runtest(suite)
        finally:
            if self.context.target:
                self.context.target.stop()

if __name__ == "__main__":
    TargetTestRunner().run()
