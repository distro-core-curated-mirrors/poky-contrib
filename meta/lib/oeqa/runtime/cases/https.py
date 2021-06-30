#
# SPDX-License-Identifier: MIT
#

import os

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.runtime.decorator.package import OEHasPackage

class HttpsTest(OERuntimeTestCase):

    @OETestDepends(["ssh.SSHTest.test_ssh"])
    @OEHasPackage(["wget", "ca-certificates"])
    def test_wget(self):
        #
        # These should pass
        #
        status, output = self.target.run("wget https://www.yoctoproject.com/")
        self.assertEqual(status, 0, msg="wget failed:\n%s" % (output))

        status, output = self.target.run("wget https://www.badssl.com/")
        self.assertEqual(status, 0, msg="wget failed:\n%s" % (output))

        status, output = self.target.run("wget https://tls-v1-2.badssl.com:1012")
        self.assertEqual(status, 0, msg="wget failed:\n%s" % (output))

        #
        # These should fail
        #
        status, output = self.target.run("wget https://self-signed.badssl.com/")
        self.assertEqual(status, 5, msg="wget didn't fail as expected:\n%s" % (output))

        status, output = self.target.run("wget https://expired.badssl.com/")
        self.assertEqual(status, 5, msg="wget didn't fail as expected:\n%s" % (output))

    @OETestDepends(["ssh.SSHTest.test_ssh"])
    @OEHasPackage(["curl", "ca-certificates"])
    def test_curl(self):
        #
        # These should pass
        #
        status, output = self.target.run("curl --output /dev/null https://www.yoctoproject.com/")
        self.assertEqual(status, 0, msg="curl failed:\n%s" % (output))

        status, output = self.target.run("curl --output /dev/null https://www.badssl.com/")
        self.assertEqual(status, 0, msg="curl failed:\n%s" % (output))

        status, output = self.target.run("curl --output /dev/null https://tls-v1-2.badssl.com:1012")
        self.assertEqual(status, 0, msg="curl failed:\n%s" % (output))

        #
        # These should fail
        #
        status, output = self.target.run("curl --output /dev/null https://self-signed.badssl.com/")
        self.assertEqual(status, 60, msg="curl didn't fail as expected:\n%s" % (output))

        status, output = self.target.run("curl --output /dev/null https://expired.badssl.com/")
        self.assertEqual(status, 60, msg="curl didn't fail as expected:\n%s" % (output))
