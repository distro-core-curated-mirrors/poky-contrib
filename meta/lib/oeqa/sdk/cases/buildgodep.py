import unittest
from oeqa.sdk.case import OESDKTestCase
from oeqa.sdk.utils.sdkbuildproject import SDKBuildProject


class BuildGoDep(OESDKTestCase):
    td_vars = ['DATETIME']

    @classmethod
    def setUpClass(self):
        dl_dir = self.td.get('DL_DIR', None)
        machine = self.td.get("MACHINE")
        self.gopath = "%s/go/" % self.tc.sdk_dir

        if not self.tc.hasHostPackage("packagegroup-go-cross-canadian-%s" % machine):
            raise unittest.SkipTest("SDK doesn't contain a Go toolchain")

        self.project = SDKBuildProject(self.gopath, self.tc.sdk_env,
                                       "https://github.com/golang/dep/archive/v0.3.1.tar.gz",
                                       self.tc.sdk_dir, self.td['DATETIME'],
                                       dl_dir=dl_dir)
        self.project.download_archive()
        # Go expects source to live in a specific sub-directory of GOPATH
        self.project._run("mkdir -p %s/src/github.com/golang" % self.gopath)
        self.project._run("mv %s/dep-0.3.1 %s/src/github.com/golang/dep" % (self.gopath, self.gopath))

    @classmethod
    def tearDownClass(self):
        self.project.clean()

    def _go_run(self, command):
        go = "export GOPATH=%s; " % self.gopath
        go = go + "cd %s/src/github.com/golang/dep; " % self.gopath
        go = go + "${CROSS_COMPILE}go "
        go = go + command
        return self.project._run(go)

    def test_godep(self):
        retval = self._go_run('build github.com/golang/dep/cmd/dep')
        self.assertEqual(retval, 0, msg="Running go build failed")
