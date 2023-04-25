#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

from oeqa.runtime.case import OERuntimeTestCase
import tempfile

class LoginTest(OERuntimeTestCase):
    def test_screenshot(self):
        with tempfile.NamedTemporaryFile(prefix="oeqa-screenshot-login", suffix=".png") as t:
            ret = self.target.runner.run_monitor("screendump", args={"filename": t.name, "format":"png"})
            self.assertEqual(ret, {"return": {}})
            import shutil
            shutil.copy(t.name, "/home/ross")
