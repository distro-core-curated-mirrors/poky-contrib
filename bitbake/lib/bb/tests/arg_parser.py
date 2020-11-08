#
# BitBake Test for the main 'bitbake' argument parser
#
# Copyright (C) 2020  Agilent Technologies, Inc.
# Author: Chris Laplante <chris.laplante@agilent.com>
#
# SPDX-License-Identifier: MIT
#

import collections
import shlex
import types
import unittest

from bb.main import create_bitbake_parser, BitBakeConfigParameters, LazyUiChoices
from bb.tinfoil import TinfoilConfigParameters

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

    def test_lazy_module_loading(self):
        # This test ensures that the bb.ui modules weren't loaded immediately upon creation of the arg parser

        # Find the UI action
        ui_actions = [action for action in self._parser._actions if action.dest == "ui"]
        if len(ui_actions) > 1:
            self.fail("Found more than one 'ui' action in the argument parser?")
        self.assertEqual(len(ui_actions), 1, "Didn't find the 'ui' action in the argument parser?")

        ui_action = ui_actions[0]
        self.assertIs(type(ui_action.type), LazyUiChoices, "'ui' action has wrong type")
        self.assertFalse(ui_action.type.has_loaded_modules, "Creation of the arg parser loaded the bb.ui modules")

    def test_tinfoil_default_ui_arg(self):
        # Ensure the default 'ui' parameter is a module, not a str
        params = TinfoilConfigParameters(config_only=True)
        self.assertIs(type(params.ui), types.ModuleType)
