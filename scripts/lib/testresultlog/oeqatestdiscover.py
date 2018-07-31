import unittest

class OeqaTestDiscover(object):

    def _discover_unittest_testsuite_testcase(self, test_dir):
        loader = unittest.TestLoader()
        testsuite_testcase = loader.discover(start_dir=test_dir, pattern='*.py')
        return testsuite_testcase

    def _generate_flat_list_of_unittest_testcase(self, testsuite):
        for test in testsuite:
            if unittest.suite._isnotsuite(test):
                yield test
            else:
                for subtest in self._generate_flat_list_of_unittest_testcase(test):
                    yield subtest

    def _get_testsuite_from_unittest_testcase(self, unittest_testcase):
        testsuite = unittest_testcase[unittest_testcase.find("(")+1:unittest_testcase.find(")")]
        return testsuite

    def _get_testcase_from_unittest_testcase(self, unittest_testcase):
        testcase = unittest_testcase[0:unittest_testcase.find("(")-1]
        testsuite = self._get_testsuite_from_unittest_testcase(unittest_testcase)
        testcase = '%s.%s' % (testsuite, testcase)
        return testcase

    def _get_testcase_list(self, unittest_testcase_list):
        testcase_list = []
        for unittest_testcase in unittest_testcase_list:
            testcase_list.append(self._get_testcase_from_unittest_testcase(str(unittest_testcase)))
        return testcase_list

    def _get_testcase_remove_pattern_list(self, testcase_remove_source_file):
        testcase_remove_pattern_list = []
        with open(testcase_remove_source_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line.find('#') == 0:
                    testcase_remove_pattern_list.append(line)
        return testcase_remove_pattern_list

    def _remove_test_case_from_removal_pattern_list(self, testcase_list, testcase_remove_pattern_list):
        print('testcase remove pattern list: %s' % testcase_remove_pattern_list)
        testcase_remove_list = []
        for testcase_remove_pattern in testcase_remove_pattern_list:
            for testcase in testcase_list:
                #print('Find testcase (%s) for %s' % (testcase, testcase_remove_pattern))
                if testcase.find(testcase_remove_pattern) == 0:
                    testcase_remove_list.append(testcase)
        print('testcase remove list: %s' % testcase_remove_list)
        for testcase_remove in testcase_remove_list:
            print('testcase_remove: %s' % testcase_remove)
            if testcase_remove in testcase_list:
                testcase_list.remove(testcase_remove)

    def get_oeqa_testcase_list(self, testcase_dir, testcase_remove_file):
        unittest_testsuite_testcase = self._discover_unittest_testsuite_testcase(testcase_dir)
        unittest_testcase_list = self._generate_flat_list_of_unittest_testcase(unittest_testsuite_testcase)
        testcase_list = self._get_testcase_list(unittest_testcase_list)
        if len(testcase_remove_file) > 0:
            testcase_remove_pattern_list = self._get_testcase_remove_pattern_list(testcase_remove_file)
            self._remove_test_case_from_removal_pattern_list(testcase_list, testcase_remove_pattern_list)
        return testcase_list

