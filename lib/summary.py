import os
import utils
from tabulate import tabulate

class BaseSummary(object):
    FAIL = 'FAIL'
    SUCCESS = 'PASS'
    SKIP = 'SKIP'

    def __init__(self):
        self._results = list()

    def addFailure(self, test):
        self._results.append((self.FAIL, test))

    def addSuccess(self, test):
        self._results.append((self.SUCCESS, test))

    def addSkip(self, test):
        self._results.append((self.SKIP, test))

    def generate(self, items):
        raise Exception

class TabulateSummary(BaseSummary):
    merge_header = ['Merge Status', 'Item']
    result_header = ['Result', 'Test Description']
    tablefmt = 'simple'

    def __init__(self):
        self._results = list()

    def generate(self, items):
        text = str()
        merge_results = [[item.status, item.resource] for item in items]
        if merge_results:
            text += "\n\n%s\n" % tabulate(merge_results, self.merge_header, tablefmt=self.tablefmt)

        test_results = [(result, test.shortDescription()) for result, test in self._results]
        if test_results:
            text += "\n\n%s\n" % tabulate(test_results, self.result_header, tablefmt=self.tablefmt)

        return text
