# Copyright (C) 2016 Intel Corporation
# Released under the MIT license (see COPYING.MIT)

from oeqa.core.case import OETestCase
from oeqa.core.decorator.depends import OETestDepends

class OETestExample(OETestCase):
    def test_example(self):
        self.logger.info('IMAGE: %s' % self.d.get('IMAGE'))
        self.assertEqual('core-image-minimal', self.d.get('IMAGE'))
        self.logger.info('ARCH: %s' % self.d.get('ARCH'))
        self.assertEqual('x86', self.d.get('ARCH'))

class OETestExampleDepend(OETestCase):
    @OETestDepends(['OETestExample.test_example'])
    def test_example_depends(self):
        pass

    def test_example_no_depends(self):
        pass
