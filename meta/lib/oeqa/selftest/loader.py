# Copyright (C) 2016 Intel Corporation
# Released under the MIT license (see COPYING.MIT)

from oeqa.core.loader import OETestLoader
from oeqa.selftest.case import OESelftestTestCase

class OESelftestTestLoader(OETestLoader):
    caseClass = OESelftestTestCase

    def _getTestCase(self, testCaseClass, tcName):
        case = super(OESelftestTestLoader, self)._getTestCase(testCaseClass, tcName)

        return case
