#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

import subprocess
from oeqa.runtime.case import OERuntimeTestCase
import tempfile
from oeqa.runtime.decorator.package import OEHasPackage

class LoginTest(OERuntimeTestCase):

    @OEHasPackage(['python3-qemu-qmp'])
    def test_screenshot(self):
        if self.td.get('MACHINE') != "qemux86-64":
            self.fail

        if bb.utils.which(os.getenv('PATH'), "convert") is not None and bb.utils.which(os.getenv('PATH'), "compare") is not None:
            with tempfile.NamedTemporaryFile(prefix="oeqa-screenshot-login", suffix=".png") as t:
                ret = self.target.runner.run_monitor("screendump", args={"filename": t.name, "format":"png"})
                # Use the meta-oe version of convert, along with it's suffix
                cmd = "convert.im7 {0} -fill white -draw 'rectangle 600,10 640,22' {1}".format(t.name, t.name)
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = proc.communicate()

                # Use the meta-oe version of compare, along with it's suffix
                cmd = "compare.im7 -metric MSE {0} {1}/meta/files/image-tests/core-image-sato-{2}.png /dev/null".format(t.name, self.td.get('COREBASE'), self.td.get('MACHINE'))
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = proc.communicate()
                diff=float(error.decode('utf-8').replace("(", "").replace(")","").split()[1])
                self.assertEqual(0, diff, "Screenshot diff is %s." % (str(diff)))
        else:
            self.fail
