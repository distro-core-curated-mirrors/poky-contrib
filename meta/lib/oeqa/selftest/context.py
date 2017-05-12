# Copyright (C) 2017 Intel Corporation
# Released under the MIT license (see COPYING.MIT)

import os

from oeqa.core.context import OETestContext, OETestContextExecutor
from oeqa.core.exception import OEQAPreRun

from oeqa.utils.commands import runCmd, get_bb_var

class OESelftestTestContext(OETestContext):
    sdk_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")

    def __init__(self, td=None, logger=None):
        super(OESelftestTestContext, self).__init__(td, logger)

class OESelftestTestContextExecutor(OETestContextExecutor):
    _context_class = OESelftestTestContext

    name = 'selftest'
    help = 'selftest test component'
    description = 'Executes selftest tests'

    default_cases = [os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cases')]
    default_test_data = None

    def register_commands(self, logger, subparsers):
        import argparse_oe

        super(OESelftestTestContextExecutor, self).register_commands(logger, subparsers)

        selftest_group = self.parser.add_argument_group('selftest options')

    def _prerun(self):
        def _check_required_env_variables(vars):
            for var in vars:
                if not os.environ.get(var):
                    self.tc.logger.error("%s is not set. Did you forget to source your build environment setup script?" % var)
                    raise OEQAPreRun

        def _check_presence_meta_selftest():
            builddir = os.environ.get("BUILDDIR")
            if os.getcwd() != builddir:
                self.logger.info("Changing cwd to %s" % builddir)
                os.chdir(builddir)

            if not "meta-selftest" in get_bb_var("BBLAYERS"):
                self.tc.logger.warn("meta-selftest layer not found in BBLAYERS, adding it")
                meta_selftestdir = os.path.join(
                    get_bb_var("BBLAYERS_FETCH_DIR"), 'meta-selftest')
                if os.path.isdir(meta_selftestdir):
                    runCmd("bitbake-layers add-layer %s" %meta_selftestdir)
                else:
                    self.tc.logger.error("could not locate meta-selftest in:\n%s" % meta_selftestdir)
                    raise OEQAPreRun

        _check_required_env_variables(["BUILDDIR"])
        _check_presence_meta_selftest()

        if "buildhistory.bbclass" in get_bb_var("BBINCLUDED"):
            self.tc.logger.error("You have buildhistory enabled already and this isn't recommended for selftest, please disable it first.")
            raise OEQAPreRun

        if get_bb_var("PRSERV_HOST"):
            self.tc.logger.error("Please unset PRSERV_HOST in order to run oe-selftest")
            raise OEQAPreRun

        if get_bb_var("SANITY_TESTED_DISTROS"):
            self.tc.logger.error("Please unset SANITY_TESTED_DISTROS in order to run oe-selftest")
            raise OEQAPreRun

        self.tc.logger.info("Running bitbake -p")
        runCmd("bitbake -p")

_executor_class = OESelftestTestContextExecutor
