#
# SPDX-License-Identifier: MIT
#

import unittest
import pprint
import datetime
import bb

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.core.decorator.data import skipIfNotFeature
from oeqa.runtime.decorator.package import OEHasPackage
from oeqa.utils.logparser import PtestParser


class PTestBase(OERuntimeTestCase):

    @classmethod
    def setUpClass(cls):
        cls.ptest_startup()

    @classmethod
    def tearDownClass(cls):
        cls.ptest_finishup()

    @classmethod
    def ptest_startup(cls):
        cls.failmsg = ""
        cls.ptests = []

        cls.test_log_dir = cls.td.get('TEST_LOG_DIR', '')
        # The TEST_LOG_DIR maybe NULL when testimage is added after
        # testdata.json is generated.
        if not cls.test_log_dir:
            cls.test_log_dir = os.path.join(cls.td.get('WORKDIR', ''), 'testimage')
        # Don't use self.td.get('DATETIME'), it's from testdata.json, not
        # up-to-date, and may cause "File exists" when re-reun.

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        cls.ptest_log_dir_link = os.path.join(cls.test_log_dir, 'ptest_log')
        cls.ptest_log_dir = '%s.%s' % (cls.ptest_log_dir_link, timestamp)
        cls.ptest_runner_log = os.path.join(cls.ptest_log_dir, 'ptest-runner.log')

        os.makedirs(cls.ptest_log_dir)

        if not hasattr(cls.tc, "extraresults"):
            cls.tc.extraresults = {}

        cls.extras = cls.tc.extraresults
        cls.extras['ptestresult.rawlogs'] = {'log': ""}
        cls.extras['ptestresult.sections'] = {}

    @classmethod
    def ptest_finishup(cls):

        # update symlink to ptest_log
        if os.path.exists(cls.ptest_log_dir_link):
            # Remove the old link to create a new one
            os.remove(cls.ptest_log_dir_link)
        os.symlink(os.path.basename(cls.ptest_log_dir), cls.ptest_log_dir_link)

        if cls.failmsg:
            cls.fail(cls.failmsg)

class PtestRunnerTest(PTestBase):
    def run_ptest(self, ptest):
        status, output = self.target.run('ptest-runner %s' % ptest, 0)
        ptest_raw_log = os.path.join(self.ptest_log_dir, "%s-raw.log" % ptest)
        with open(ptest_raw_log, 'w') as f:
            f.write(output)

        # Parse and save results
        parser = PtestParser()
        results, sections = parser.parse(ptest_raw_log)
        parser.results_as_files(self.ptest_log_dir)

        self.extras['ptestresult.rawlogs']['log']  = self.extras['ptestresult.rawlogs']['log'] + output
        try:
            self.extras['ptestresult.sections'][ptest]  = sections[ptest]
        except KeyError:
            bb.warn("ptest %s timedout or crashed for some reason. Check the log: %s" % (ptest, self.ptest_log_dir))
            return

        trans = str.maketrans("()", "__")
        for section in results:
            for test in results[section]:
                result = results[section][test]
                testname = "ptestresult." + (section or "No-section") + "." + "_".join(test.translate(trans).split())
                self.extras[testname] = {'status': result}

        failed_tests = {}
        for section in results:
            failed_testcases = [ "_".join(test.translate(trans).split()) for test in results[section] if results[section][test] == 'fail' ]
            if failed_testcases:
                failed_tests[section] = failed_testcases

        status, output = self.target.run('dmesg | grep "Killed process"', 0)
        if output:
            self.failmsg = "ERROR: Processes were killed by the OOM Killer:\n%s\n" % output

        if failed_tests:
            self.failmsg = self.failmsg + "Failed ptests:\n%s" % pprint.pformat(failed_tests)


    @skipIfNotFeature('ptest', 'Test requires ptest to be in DISTRO_FEATURES')
    @OETestDepends(['ssh.SSHTest.test_ssh'])
    @OEHasPackage(['ptest-runner'])
    def test_ptestrunner_check(self):
        status, output = self.target.run('which ptest-runner')
        msg = 'ptest-runner not installed .  %s' % output
        self.assertEqual(status, 0, msg=msg)

    @OETestDepends(['ptest.PtestRunnerTest.test_ptestrunner_check'])
    def test_ptests_installed(self):
        status, output = self.target.run('ptest-runner -l')
        msg = 'No ptests found.  %s' % output
        self.assertEqual(status, 0, msg=msg)

        # built ptest list
        for ptest in output.split("\n"):
            if ptest.startswith("Available"):
                continue
            self.ptests.append(ptest.split()[0])

    @OETestDepends(['ptest.PtestRunnerTest.test_ptests_installed'])
    @unittest.expectedFailure
    def test_ptestrunner(self):
        for ptest in self.ptests:
            self.run_ptest(ptest)
