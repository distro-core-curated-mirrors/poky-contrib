import os
import utils
from tabulate import tabulate

class BasicSummary(dict):
    merge_header = ['Merge Status', 'Item']
    result_header = ['Result', 'Test Description', 'Assertion Description']
    tablefmt = 'simple'

    def __init__(self):
        self._results = list()

    def addFailure(self, test, err):
        _, assertionDescription, _ = err
        self._results.append(['FAIL: ', test.shortDescription()])

    def addSuccess(self, test):
        self._results.append(['PASS: ', test.shortDescription()])

    def addSkip(self, test, msg):
        self._results.append(['SKIP: ', test.shortDescription()])

    def generateSummary(self, items):
        """ Generate and store the summary """
        text = ''
        if items:
            merge_results = [[item.status, item.resource] for item in items]
            text += "\n\n%s\n" % tabulate(merge_results, BasicSummary.merge_header, tablefmt=BasicSummary.tablefmt)

        text += "\n\n%s\n" % tabulate(self._results, BasicSummary.result_header, tablefmt=BasicSummary.tablefmt)

        return text
