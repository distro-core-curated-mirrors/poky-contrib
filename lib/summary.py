import os
import utils
from tabulate import tabulate

class BasicSummary(dict):
    header = ['Result', 'Item', 'Test Description', 'Assertion Description']
    tablefmt = 'simple'

    def __init__(self, item):
        self._item = item

        self._results = list()
        self._patchmsg = None

    def addPatchFailure(self, msg):
        self._patchmsg = msg

    def addFailure(self, test, err):
        _, assertionDescription, _ = err
        self._results.append(['FAIL: ', self._item, test.shortDescription(), assertionDescription])

    def addSuccess(self, test):
        self._results.append(['PASS: ', self._item, test.shortDescription(), ''])

    def generateSummary(self):
        """ Generate and store the summary """
        summary = ""

        if self._patchmsg:
            summary += "%s" % self._patchmsg
        else:
            summary += "%s\n" % tabulate(self._results, BasicSummary.header, tablefmt=BasicSummary.tablefmt)
        return summary
