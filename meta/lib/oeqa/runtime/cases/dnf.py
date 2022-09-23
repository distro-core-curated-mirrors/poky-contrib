#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

import os
from oeqa.utils.httpserver import HTTPService

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.core.decorator.data import skipIfNotDataVar, skipIfNotFeature
from oeqa.runtime.decorator.package import OEHasPackage

from oeqa.utils.subprocesstweak import errors_have_output
errors_have_output()

class DnfTest(OERuntimeTestCase):
    @classmethod
    def create_rpm_index(cls):
        import glob
        import subprocess
        import oe

        archs = (cls.tc.td['ALL_MULTILIB_PACKAGE_ARCHS'] or '').replace('-', '_')
        for arch in archs.split():
            rpm_dir = os.path.join(cls.tc.td['DEPLOY_DIR_RPM'], arch)
            idx_path = os.path.join(cls.tc.td['WORKDIR'], 'oe-testimage-repo', arch)

            if not os.path.isdir(rpm_dir):
                continue

            lockfilename = os.path.join(cls.tc.td['DEPLOY_DIR_RPM'], 'rpm.lock')
            lf = bb.utils.lockfile(lockfilename, False)
            oe.path.copyhardlinktree(rpm_dir, idx_path)
            # Full indexes overload a 256MB image so reduce the number of rpms
            # in the feed by filtering to specific packages needed by the tests.
            package_list = glob.glob(os.path.jon(idx_path, "*", "*.rpm"))

            for pkg in package_list:
                basename = os.path.basename(pkg)
                if basename.startswith("curl-ptest") or not basename.startswith("curl"):
                    bb.utils.remove(pkg)

            bb.utils.unlockfile(lf)

            # Create repodata
            try:
                cmd = 'createrepo_c --update -q %s' % (idx_path)
                bb.note("Executing '%s'" % cmd)
                subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
            except subprocess.CalledProcessError as e:
                bb.fatal("Index creation failed with return code %d: %s" % (e.returncode, e.output))

    @classmethod
    def setUpClass(cls):
        cls.create_rpm_index()
        #repo_dir = cls.tc.td['DEPLOY_DIR_RPM']
        repo_dir = os.path.join(cls.tc.td['WORKDIR'], 'oe-testimage-repo')
        cls.repo_server = HTTPService(repo_dir, '0.0.0.0', port=cls.tc.target.server_port, logger=cls.tc.logger)
        cls.repo_server.start()

    @classmethod
    def tearDownClass(cls):
        cls.repo_server.stop()

    def dnf(self, command, expected = 0):
        command = 'dnf %s' % command
        status, output = self.target.run(command, 1500)
        message = os.linesep.join([command, output])
        self.assertEqual(status, expected, message)
        return output

    def dnf_with_repo(self, command):
        pkgarchs = os.listdir(os.path.join(self.tc.td['WORKDIR'], 'oe-testimage-repo'))
        deploy_url = 'http://%s:%s/' %(self.target.server_ip, self.repo_server.port)
        cmdlinerepoopts = ["--repofrompath=oe-testimage-repo-%s,%s%s" %(arch, deploy_url, arch) for arch in pkgarchs]

        output = self.dnf(" ".join(cmdlinerepoopts) + " --nogpgcheck " + command)
        return output

    @skipIfNotFeature('package-management',
                      'Test requires package-management to be in IMAGE_FEATURES')
    @skipIfNotDataVar('IMAGE_PKGTYPE', 'rpm',
                      'RPM is not the primary package manager')
    @OEHasPackage(['dnf'])
    @OETestDepends(['ssh.SSHTest.test_ssh'])
    def test_dnf_help(self):
        self.dnf('--help')

    @OETestDepends(['dnf.DnfTest.test_dnf_help'])
    def test_dnf_makecache(self):
        self.dnf_with_repo('makecache')

    @OETestDepends(['dnf.DnfTest.test_dnf_makecache'])
    def test_dnf_repoinfo(self):
        output = self.dnf_with_repo('repoinfo')
        self.assertIn("Added oe-testimage-repo-noarch", output)

    @OETestDepends(['dnf.DnfTest.test_dnf_makecache'])
    def test_dnf_install(self):
        self.dnf_with_repo('remove -y curl-dev')
        self.dnf_with_repo('install -y curl-dev')

    @OETestDepends(['dnf.DnfTest.test_dnf_makecache'])
    def test_dnf_reinstall(self):
        self.dnf_with_repo('reinstall -y curl')

    @OETestDepends(['dnf.DnfTest.test_dnf_makecache'])
    def test_dnf_exclude(self):
        self.dnf_with_repo('remove -y curl-dev')
        self.dnf_with_repo('install -y --exclude=curl-dev curl*')
        output = self.dnf('list --installed curl*')
        self.assertIn("curl.", output)
        self.assertNotIn("curl-dev.", output)
