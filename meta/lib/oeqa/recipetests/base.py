import os
import shutil
from oeqa.selftest.base import oeSelfTest
import oeqa.utils.ftools as ftools


class RecipeTests(oeSelfTest):

    def __init__(self, methodName="runTest"):
        super(RecipeTests, self).__init__(methodName)
        self.testinc_path = os.path.join(self.builddir, 'conf/testrecipe.inc')
        self.required_path = os.path.join(self.builddir, 'conf/required.inc')
        self.testrecipe = os.getenv("TESTRECIPE")

        # Use a clean TMPDIR for each run
        tmpdir_name = self.builddir + '/tmp_' + self.testrecipe
        shutil.rmtree(tmpdir_name, ignore_errors=True)

        feature = 'TMPDIR = "%s"\n' % tmpdir_name
        self.set_required_config(feature)

    # write to <builddir>/conf/requred.inc
    def set_required_config(self, data):
        self.log.debug("Writing to: %s\n%s\n" % (self.required_path, data))
        ftools.write_file(self.required_path, data)
