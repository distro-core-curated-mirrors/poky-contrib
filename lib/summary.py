import os
import utils
from tabulate import tabulate

class BasicSummary(dict):
    header = ['Result', 'Test Description', 'Assertion Description']
    tablefmt = 'simple'

    def __init__(self, items):
        self._items = items

        self._results = list()
        self._patchmsg = None

    def addPatchFailure(self, msg):
        self._patchmsg = msg

    def addFailure(self, test, err):
        _, assertionDescription, _ = err
        self._results.append(['FAIL: ', test.shortDescription(), assertionDescription])

    def addSuccess(self, test):
        self._results.append(['PASS: ', test.shortDescription(), ''])

    def addSkip(self, test, msg):
        self._results.append(['SKIP: ', test.shortDescription(), msg])

    def generateSummary(self):
        """ Generate and store the summary """

        summary = "Tested items:\n\n"
        for item in self._items:
            summary += "\t%s\n" % item
        summary +="\n\n"

        if self._patchmsg:
            summary += "%s" % self._patchmsg
        else:
            summary += "%s\n" % tabulate(self._results, BasicSummary.header, tablefmt=BasicSummary.tablefmt)
        return summary
