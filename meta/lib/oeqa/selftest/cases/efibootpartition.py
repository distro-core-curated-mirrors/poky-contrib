# Based on runqemu.py test file
#
# Copyright (c) 2017 Wind River Systems, Inc.
#
# SPDX-License-Identifier: MIT
#

from functools import wraps, lru_cache
import unittest

from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, get_bb_var, runqemu

def only_for_arch(archs):
    """Decorator for wrapping test cases that can be run only for specific target
    architectures. A list of compatible architectures is passed in `archs`.
    """

    @lru_cache()
    def get_host_arch():
        return get_bb_var('HOST_ARCH')

    def wrapper(func):
        @wraps(func)
        def wrapped_f(*args, **kwargs):
            arch = get_host_arch()
            if archs and arch not in archs:
                raise unittest.SkipTest("Testcase arch dependency not met: %s" % arch)
            return func(*args, **kwargs)
        return wrapped_f
    return wrapper

class GenericEFITest(OESelftestTestCase):
    """EFI booting test class"""
    @only_for_arch(['i586', 'i686', 'x86_64'])
    def test_boot_efi(self):
        cmd_common = "runqemu nographic serial wic ovmf"
        efi_provider = "systemd-boot"
        image = "core-image-minimal"
        machine = "qemux86-64"

        self.write_config(self,
"""
EFI_PROVIDER = "%s"
IMAGE_FSTYPES:pn-%s:append = " wic"
MACHINE = "%s"
MACHINE_FEATURES:append = " efi"
WKS_FILE = "efi-bootdisk.wks.in"
IMAGE_INSTALL:append = " grub-efi systemd-boot kernel-image-bzimage"
"""
% (self.efi_provider, self.image, self.machine))

        bitbake("ovmf")
        bitbake(self.image)

        cmd = "%s %s" % (self.cmd_common, self.machine)
        with runqemu(self.image, ssh=False, launch_cmd=cmd) as qemu:
            self.assertTrue(qemu.runner.logged, "Failed: %s" % cmd)
