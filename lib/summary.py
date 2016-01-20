import os
import utils

class BasicSummary(dict):

    def __init__(self, series, revision, mbox):
        self.series = series
        self.revision = revision
        self.mbox = mbox

        self.error = list()
        self.failure = list()
        self.success = list()
        self.patchmsg = None

    def addPatchFailure(self, msg):
        self.patchmsg = msg

    def addFailure(self, test, err):
        self.failure.append((test,err))

    def addSuccess(self, test):
        self.success.append(test)

    def generateSummary(self):
        """ Generate and store the summary """
        summary = ""

        if self.patchmsg:
            summary += "%s" % self.patchmsg
        else:
            summary  += "Tested mbox: %s\n" % self.mbox
            if self.success:
                summary += "\nPass:\n"
                for test in self.success:
                    summary += "\t%s\n" % test

            if self.failure:
                summary += "\nFail:\n"
                for test, err in self.failure:
                    (ty, va, trace) = err
                    summary += "\t%s : %s\n" % (test, va)

        return summary
