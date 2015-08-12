#!/usr/bin/python

# Copyright

# DESCRIPTION
# This is script for running all selected toaster cases on
# selected web browsers manifested in toaster_test.cfg.

# 1. How to start toaster in yocto:
# $ source poky/oe-init-build-env
# $ source toaster start
# $ bitbake core-image-minimal

# 2. How to install selenium and additional modules on Ubuntu:
# $ sudo apt-get install scrot python-pip
# $ sudo pip install selenium
# $ sudo pip install page_objects

# 3. How to install selenium addon in firefox:
# Download the lastest firefox addon from http://release.seleniumhq.org/selenium-ide/
# Then install it. You can also install firebug and firepath addon

# 4. How to start writing a new case:
# All you need to do is to implement the function test_xxx() and  pile it on.

# 5. How to test with Chrome browser
# Download/install chrome on host
# Download chromedriver from https://code.google.com/p/chromedriver/downloads/list  according to your host type
# put chromedriver in PATH, (e.g. /usr/bin/, bear in mind to chmod)
# For windows host, you may put chromedriver.exe in the same directory as chrome.exe

# 6. How to run the tests
# run single test: python -m unittest toaster_tests.ToasterTests.test_xxx (xxx) represents testcase number
# run all tests: python toaster_test_runner.py runs all the tests defined in toaster_test.cfg, cases_to_run paramater

from toaster_tests.toaster_tests import *


class ToasterTestRunner(object):
    def __init__(self):
        self.start_time = None
        self.log = LOG
        self.passed = 0
        self.failed = 0

    def run_test(self, test_case_class, test_method_name):
        suite = unittest.TestSuite()
        suite.addTest(test_case_class(test_method_name))
        runner = unittest.TextTestRunner()
        result = runner.run(suite)
        return result

    def run_all_tests(self):
        self.start_time = time.strptime(time.ctime())
        for test_case in ToasterTestsConfig.cases_to_run:
            result = self.run_test(ToasterTests, self.get_test_method_name(test_case))
            self.log_test_result(result)
        self.log_aggregate_results()
        self.collect_log()

    def get_test_method_name(self, test_case):
        return "test_" + str(test_case)

    def log_test_result(self, result):
        if result.wasSuccessful():
            self.log.info("Test PASSED")
            self.passed += 1
            return
        self.failed += 1
        if len(result.errors) > 0:
            self.log.error("Testcase errors:")
            for error in result.errors:
                self.log.error(error[1])
        if len(result.failures) > 0:
            self.log.error("Testcase failures:")
            for failure in result.failures:
                self.log.error(failure[1])

    def log_aggregate_results(self):
        self.log.info(const.LOG_AGGREGATE_RESULTS
                      .replace("$TOTAL_TESTS", str(self.passed + self.failed))
                      .replace("$FAILED_TESTS", str(self.failed))
                      .replace("$PASSED_TESTS", str(self.passed)))

    def collect_log(self):
        """
        the log files are temporarily stored in ./log/tmp/..
        After all cases are done, they should be transfered to ./log/$TIMESTAMP/
        """
        now = self.start_time
        now_str = "%d-%02d-%02d-%02d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday,
                                                   now.tm_hour, now.tm_min, now.tm_sec)
        try:
            print const.TMP_LOG_DIR_PATH, os.path.join(os.path.dirname(const.TMP_LOG_DIR_PATH), now_str)
            os.rename(const.TMP_LOG_DIR_PATH,
                      os.path.join(os.path.dirname(const.TMP_LOG_DIR_PATH), now_str))
        except:
            self.log.error("Cannot create log dir %s under %s, please check your privilege" % (now_str, const.LOG_DIR_PATH))


if __name__ == "__main__":
    runner = ToasterTestRunner()
    runner.run_all_tests()