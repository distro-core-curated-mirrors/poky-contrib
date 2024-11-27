#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

# This class is used by the yocto-check-layer script for additional
# per-recipe tests.
#
# It adds an anonymous python function with extra processing to all recipes,
# globally inheriting this class isn't advisable - yocto-check-layer script
# handles that during its signature dump


# Ensure that recipes don't skip required QA checks as listed
# in CHECKLAYER_REQUIRED_TESTS, defined by insane.bbclass
def check_insane_skip(d):
    required_tests = set((d.getVar('CHECKLAYER_REQUIRED_TESTS') or '').split())
    packages = set((d.getVar('PACKAGES') or '').split())
    for package in packages:
        skip = set((d.getVar('INSANE_SKIP') or "").split() +
                   (d.getVar('INSANE_SKIP:' + package) or "").split())
        skip_required = skip & required_tests
        if skip_required:
            oe.qa.write_error(" ".join(skip_required), 'Package %s is skipping required QA tests.' % package, d)
            bb.error("QA Issue: %s [%s]" % ('Package %s is skipping required QA tests.' % package, " ".join(skip_required)))
            d.setVar("QA_ERRORS_FOUND", "True")


# Check that only approved tasks can reach the network
def check_network_flag(d):
    # BPN:task names that are allowed to reach the network, using fnmatch to compare.
    allowed = []
    # fetch and checkuri by definition need to reach the network
    allowed += ["*:do_fetch", "*:do_checkuri"]
    # The tests need to SSH to their target and download tarballs
    allowed += ["*:do_testimage", "*:do_testsdk", "*:do_testsdkext"]
    # devshell needs to be unconstrained
    allowed += ["*:do_devshell", "*:do_pydevshell"]

    # Recipe-specific tasks in oe-core that we allow:
    # The toolchain tests need to SSH to their target
    allowed += ["binutils*:do_check", "gcc*:do_check", "glibc*:do_check"]
    # build-appliance-image uses pip at image time
    allowed += ["build-appliance-image:do_image"]

    def is_allowed(bpn, task):
        from fnmatch import fnmatch
        name = f"{bpn}:{task}"
        return any(fnmatch(name, pattern) for pattern in allowed)

    bpn = d.getVar("BPN")
    for task in bb.build.listtasks(d):
        network = bb.utils.to_boolean(d.getVarFlag(task, "network"))
        if network and not is_allowed(bpn, task):
            bb.error(f"QA Issue: task {task} has network enabled")


python () {
    check_insane_skip(d)
    check_network_flag(d)
}
