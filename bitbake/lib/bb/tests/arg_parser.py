#
# BitBake Test for the main 'bitbake' argument parser
#
# Copyright (C) 2020  Agilent Technologies, Inc.
# Author: Chris Laplante <chris.laplante@agilent.com>
#
# SPDX-License-Identifier: MIT
#

import unittest

from bb.main import create_bitbake_parser


class ArgParserTests(unittest.TestCase):
    def setUp(self):
        self._parser = create_bitbake_parser()
