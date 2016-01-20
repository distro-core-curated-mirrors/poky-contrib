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
        self.patcherror = None

    def patchFailure(self, err):
        self.patcherror = err

    def addFailure(self, test, err):
        self.failure.append((test,err))

    def addSuccess(self, test):
        self.success.append(test)

    def generateSummary(self):
        """ Generate and store the summary """
        self._summary  = "Tested mbox: %s\n" % self.mbox
        
        if self.patcherror:
            (_, exception, _) = self.patcherror
            self._summary += "\n\t%s" % exception
        else:
            if self.success:
                self._summary += "\nPass:\n"
                for test in self.success:
                    self._summary += "\t%s\n" % test

            if self.failure:
                self._summary += "\nFail:\n"
                for test, err in self.failure:
                    (ty, va, trace) = err
                    self._summary += "\t%s : %s\n" % (test, va)

        return self._summary
