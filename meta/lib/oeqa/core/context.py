# Copyright (C) 2016 Intel Corporation
# Released under the MIT license (see COPYING.MIT)

import os
import sys
import json
import time
import logging
import collections

from oeqa.core.loader import OETestLoader
from oeqa.core.runner import OETestRunner, OEStreamLogger

class OETestContext(object):
    loaderClass = OETestLoader
    runnerClass = OETestRunner

    files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../files")

    def __init__(self, d=None, logger=None):
        if not type(d) is dict:
            raise TypeError("d isn't dictionary type")

        self.d = d
        self.logger = logger
        self._registry = {}
        self._registry['cases'] = collections.OrderedDict()
        self._results = {}

    def _read_modules_from_manifest(self, manifest):
        if not os.path.exists(manifest):
            raise

        modules = []
        for line in open(manifest).readlines():
            line = line.strip()
            if line and not line.startswith("#"):
                modules.append(line)

        return modules

    def loadTests(self, module_paths, modules=[], tests=[],
            modules_manifest="", modules_required=[], filters={}):
        if modules_manifest:
            modules = self._read_modules_from_manifest(modules_manifest)

        self.loader = self.loaderClass(self, module_paths, modules, tests,
                modules_required, filters)
        self.suites = self.loader.discover()

    def runTests(self):
        streamLogger = OEStreamLogger(self.logger)
        self.runner = self.runnerClass(self, stream=streamLogger, verbosity=2)
        return self.runner.run(self.suites)
