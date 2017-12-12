from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import runCmd, bitbake, get_bb_var, get_bb_vars
from oeqa.utils.decorators import testcase
from oeqa.utils.ftools import write_file
from oeqa.core.decorator.oeid import OETestID

class Distrodata(OESelftestTestCase):

    @classmethod
    def setUpClass(cls):
        super(Distrodata, cls).setUpClass()
        feature = 'INHERIT += "distrodata"\n'
        feature += 'LICENSE_FLAGS_WHITELIST += " commercial"\n'

        cls.write_config(cls, feature)
        bitbake('-c checkpkg world')


    @OETestID(1902)
    def test_checkpkg(self):
        """
        Summary:     Test that upstream version checks do not regress
        Expected:    Upstream version checks should succeed except for the recipes listed in the exception list.
        Product:     oe-core
        Author:      Alexander Kanavin <alexander.kanavin@intel.com>
        """
        checkpkg_result = open(os.path.join(get_bb_var("LOG_DIR"), "checkpkg.csv")).readlines()[1:]
        regressed_failures = [pkg_data[0] for pkg_data in [pkg_line.split('\t') for pkg_line in checkpkg_result] if pkg_data[11] == 'UNKNOWN_BROKEN']
        regressed_successes = [pkg_data[0] for pkg_data in [pkg_line.split('\t') for pkg_line in checkpkg_result] if pkg_data[11] == 'KNOWN_BROKEN']
        msg = ""
        if len(regressed_failures) > 0:
            msg = msg + """
The following packages failed upstream version checks. Please fix them using UPSTREAM_CHECK_URI/UPSTREAM_CHECK_REGEX
(when using tarballs) or UPSTREAM_CHECK_GITTAGREGEX (when using git). If an upstream version check cannot be performed
(for example, if upstream does not use git tags), you can set UPSTREAM_VERSION_UNKNOWN to '1' in the recipe to acknowledge
that the check cannot be performed.
""" + "\n".join(regressed_failures)
        if len(regressed_successes) > 0:
            msg = msg + """
The following packages have been checked successfully for upstream versions,
but their recipes claim otherwise by setting UPSTREAM_VERSION_UNKNOWN. Please remove that line from the recipes.
""" + "\n".join(regressed_successes)
        self.assertTrue(len(regressed_failures) == 0 and len(regressed_successes) == 0, msg)

    def test_maintainers(self):
        """
        Summary:     Test that recipes have a maintainer
        Expected:    All recipes (except a few special static/testing ones) should have a maintainer listed in maintainers.inc file.
        Product:     oe-core
        Author:      Alexander Kanavin <alexander.kanavin@intel.com>
        """
        def is_exception(pkg):
            exceptions = ["packagegroup-", "initramfs-", "systemd-machine-units", "container-image-testpkg", "postinst", "devtool-test-", "selftest-ed"]
            for i in exceptions:
                 if i in pkg:
                     return True
            return False

        checkpkg_result = open(os.path.join(get_bb_var("LOG_DIR"), "checkpkg.csv")).readlines()[1:]
        no_maintainer_list = [pkg_data[0] for pkg_data in [pkg_line.split('\t') for pkg_line in checkpkg_result] if pkg_data[14] == '' and not is_exception(pkg_data[0])]
        msg = """
The following packages do not have a maintainer assigned to them. Please add an entry to meta/conf/distro/include/maintainers.inc file.
""" + "\n".join(no_maintainer_list)
        self.assertTrue(len(no_maintainer_list) == 0, msg)
