#
# BitBake Test for the main 'bitbake' argument parser
#
# Copyright (C) 2020  Agilent Technologies, Inc.
# Author: Chris Laplante <chris.laplante@agilent.com>
#
# SPDX-License-Identifier: MIT
#

import shlex
import unittest
import collections


from bb.main import create_bitbake_parser, BitBakeConfigParameters

ParseResult = collections.namedtuple("ParseResult", ("options", "targets"))


class ArgParserTests(unittest.TestCase):
    def setUp(self):
        self._parser = create_bitbake_parser()

    def _parse_helper(self, arg_str):
        self.assertIs(type(arg_str), str)
        params = BitBakeConfigParameters(argv=shlex.split(arg_str))
        return ParseResult(params.options, params.options.pkgs_to_build)

    def test_parse_s_none_world(self):
        # All of these should give the same result
        arg_strs = [
            "bitbake -S none world",
            "bitbake world -S none",
            "bitbake -Snone world",
            # optparse doesn't handle =
            # "bitbake -S=none world",
            # "bitbake world -S=none"
        ]

        for arg_str in arg_strs:
            res = self._parse_helper(arg_str)
            self.assertListEqual(res.targets, ["world"])
            self.assertListEqual(res.options.dump_signatures, ["none"])
