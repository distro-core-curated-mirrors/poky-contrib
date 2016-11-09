# Copyright (C) 2016 Intel Corporation
# Released under the MIT license (see COPYING.MIT)

from oeqa.core.case import OETestCase
from oeqa.core.decorator.oetag import OETestTag
from oeqa.core.decorator.data import OETestDataDepends

class DataTest(OETestCase):
    data_vars = ['IMAGE', 'ARCH']

    @OETestDataDepends(['MACHINE',])
    @OETestTag('dataTestOk')
    def testDataOk(self):
        self.assertEqual(self.d.get('IMAGE'), 'core-image-minimal')
        self.assertEqual(self.d.get('ARCH'), 'x86')
        self.assertEqual(self.d.get('MACHINE'), 'qemuarm')

    @OETestTag('dataTestFail')
    def testDataFail(self):
        pass
