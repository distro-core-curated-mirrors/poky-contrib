import os
import utils
from tabulate import tabulate

class BasicSummary(dict):

    def __init__(self, commit, branch, mbox):
        self.commit = commit
        self.branch = branch
        self.mbox = mbox

        self.results= list()
        self.patchmsg = None

    def addPatchFailure(self, msg):
        self.patchmsg = msg

    def addFailure(self, test, err):
        _, va, _ = err
        self.results.append(['FAIL: ', test.id(), test.shortDescription(), va])

    def addSuccess(self, test):
        self.results.append(['PASS: ', test.id(), test.shortDescription(), None])

    def generateSummary(self):
        """ Generate and store the summary """
        summary = ""

        if self.patchmsg:
            summary += "%s" % self.patchmsg
        else:
            if self.mbox:
                summary += "Tested mbox: %s\n\n" % self.mbox
            else:
                summary += "Tested branch/commit: %s/%s\n\n" % (self.branch, self.commit)
            summary += tabulate(self.results)

        return summary
