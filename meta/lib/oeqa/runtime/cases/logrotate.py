#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

# This test should cover https://bugzilla.yoctoproject.org/tr_show_case.cgi?case_id=289 testcase
# Note that the image under test must have logrotate installed

from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.runtime.decorator.package import OEHasPackage

class LogrotateTest(OERuntimeTestCase):

    @classmethod
    def setUpClass(cls):
        cls.tc.target.run('test -f /etc/logrotate.d/wtmp && cp /etc/logrotate.d/wtmp $HOME/wtmp.oeqabak', ignore_status=True)

    @classmethod
    def tearDownClass(cls):
        cls.tc.target.run('test -f $HOME/wtmp.oeqabak && mv -f $HOME/wtmp.oeqabak /etc/logrotate.d/wtmp', ignore_status=True)
        cls.tc.target.run('rm -rf /var/log/logrotate_dir /var/log/logrotate_testfile /etc/logrotate.d/logrotate_testfile')

    @OETestDepends(['ssh.SSHTest.test_ssh'])
    @OEHasPackage(['logrotate'])
    def test_logrotate_wtmp(self):
        # /var/log/wtmp may not always exist initially, so use touch to ensure it is present
        self.target.run('touch /var/log/wtmp')

        self.target.run('mkdir /var/log/logrotate_dir')

        self.target.run('echo "create \n olddir /var/log//logrotate_dir \n include /etc/logrotate.d/wtmp" > /tmp/logrotate-test.conf')
        
        # If logrotate fails to rotate the log, view the verbose output of logrotate to see what prevented it
        self.target.run('logrotate -vf /tmp/logrotate-test.conf')
        status, _ = self.target.run('find /var/log//logrotate_dir -type f | grep wtmp.1')

    @OETestDepends(['logrotate.LogrotateTest.test_logrotate_wtmp'])
    def test_logrotate_newlog(self):
        self.target.run('echo "oeqa logrotate test file" > /var/log/logrotate_testfile')
        
        self.target.run('echo "/var/log/logrotate_testfile {\n missingok \n monthly \n rotate 1" > /etc/logrotate.d/logrotate_testfile')

        self.target.run('echo "create \n olddir /var/log//logrotate_dir \n include /etc/logrotate.d/logrotate_testfile" > /tmp/logrotate-test2.conf')

        status, output = self.target.run('find /var/log//logrotate_dir -type f | grep logrotate_testfile.1')
        msg = ('A rotated log for logrotate_testfile is already present in logrotate_dir')
        self.assertEqual(status, 1, msg = msg)

        # If logrotate fails to rotate the log, view the verbose output of logrotate instead of just listing the files in olddir
        _, logrotate_output = self.target.run('logrotate -vf /tmp/logrotate-test2.conf')
        status, _ = self.target.run('find /var/log//logrotate_dir -type f | grep logrotate_testfile.1')
        msg = ('logrotate did not successfully rotate the logrotate_test log. Output from logrotate -vf: \n%s' % (logrotate_output))
        self.assertEqual(status, 0, msg = msg)
