#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

import os
import fnmatch
import time

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.core.decorator.data import skipIfDataVar
from oeqa.runtime.decorator.package import OEHasPackage
from oeqa.core.utils.path import findFile

class RpmBasicTest(OERuntimeTestCase):

    @OEHasPackage(['rpm'])
    @OETestDepends(['ssh.SSHTest.test_ssh'])
    def test_rpm_help(self):
        status, output = self.target.run('rpm --help')
        msg = 'status and output: %s and %s' % (status, output)
        self.assertEqual(status, 0, msg=msg)

    @OETestDepends(['rpm.RpmBasicTest.test_rpm_help'])
    def test_rpm_query(self):
        status, output = self.target.run('ls /var/lib/rpm/')
        if status != 0:
            self.skipTest('No /var/lib/rpm on target')
        status, output = self.target.run('rpm -q rpm')
        msg = 'status and output: %s and %s' % (status, output)
        self.assertEqual(status, 0, msg=msg)

    @OETestDepends(['rpm.RpmBasicTest.test_rpm_query'])
    def test_rpm_query_nonroot(self):

        def set_up_test_user(u):
            self.target.run('id -u %s || useradd %s' % (u, u))

        def exec_as_test_user(u):
            self.target.run('su -c id %s' % u)

            self.target.run('su -c "rpm -qa" %s ' % u)

        def wait_for_no_process_for_user(u, timeout = 120):
            timeout_at = time.time() + timeout
            while time.time() < timeout_at:
                _, output = self.target.run(self.tc.target_cmds['ps'])
                if u + ' ' not in output:
                    return
                time.sleep(1)
            user_pss = [ps for ps in output.split("\n") if u + ' ' in ps]
            msg = "User %s has processes still running: %s" % (u, "\n".join(user_pss))
            self.fail(msg=msg)

        def unset_up_test_user(u):
            # ensure no test1 process in running
            wait_for_no_process_for_user(u)
            status, output = self.target.run('userdel -r %s' % u)
            msg = 'Failed to erase user: %s' % output
            self.assertTrue(status == 0, msg=msg)

        tuser = 'test1'

        try:
            set_up_test_user(tuser)
            exec_as_test_user(tuser)
        finally:
            unset_up_test_user(tuser)


class RpmInstallRemoveTest(OERuntimeTestCase):

    @classmethod
    def setUpClass(cls):
        pkgarch = cls.td['TUNE_PKGARCH'].replace('-', '_')
        rpmdir = os.path.join(cls.tc.td['DEPLOY_DIR'], 'rpm', pkgarch)
        # Pick base-passwd-doc as a test file to get installed, because it's small
        # and it will always be built for standard targets
        rpm_doc = 'base-passwd-doc-*.%s.rpm' % pkgarch
        if not os.path.exists(rpmdir):
            return
        for f in fnmatch.filter(os.listdir(rpmdir), rpm_doc):
            cls.test_file = os.path.join(rpmdir, f)
        cls.dst = '/tmp/base-passwd-doc.rpm'

    @OETestDepends(['rpm.RpmBasicTest.test_rpm_query'])
    def test_rpm_install(self):
        self.tc.target.copyTo(self.test_file, self.dst)
        self.target.run('rpm -ivh /tmp/base-passwd-doc.rpm')
        self.tc.target.run('rm -f %s' % self.dst)

    @OETestDepends(['rpm.RpmInstallRemoveTest.test_rpm_install'])
    def test_rpm_remove(self):
        self.target.run('rpm -e base-passwd-doc')

    @OETestDepends(['rpm.RpmInstallRemoveTest.test_rpm_remove'])
    def test_check_rpm_install_stress(self):
        self.tc.target.copyTo(self.test_file, self.dst)

        # Install/Remove a package 10 times
        for i in range(10):
            self.target.run('rpm -ifvh /tmp/base-passwd-doc.rpm')
            self.target.run('rpm -e base-passwd-doc')

        self.tc.target.run('rm -f %s' % self.dst)
