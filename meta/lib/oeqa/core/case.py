# Copyright (C) 2016 Intel Corporation
# Released under the MIT license (see COPYING.MIT)

import unittest

from oeqa.core.exception import OEQAMissingVariable

def _validate_data_vars(d, data_vars, type_msg):
    if data_vars:
        for v in data_vars:
            if not v in d:
                raise OEQAMissingVariable("Test %s need %s variable but"\
                        " isn't into d" % (type_msg, v))

class OETestCase(unittest.TestCase):
    # TestContext and Logger instance set by OETestLoader.
    tc = None
    logger = None

    # d has all the variables needed by the test cases
    # is the same across all the test cases.
    d = None

    # data_vars has the variables needed by a test class
    # or test case instance, if some var isn't into d a
    # OEMissingVariable exception is raised
    data_vars = None

    @classmethod
    def _oeSetUpClass(clss):
        _validate_data_vars(clss.d, clss.data_vars, "class")
        clss.setUpClassMethod()

    @classmethod
    def _oeTearDownClass(clss):
        clss.tearDownClassMethod()

    def _oeSetUp(self):
        for d in self.decorators:
            d.setUpDecorator()
        self.setUpMethod()

    def _oeTearDown(self):
        for d in self.decorators:
            d.tearDownDecorator()
        self.tearDownMethod()
