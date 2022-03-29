# Based on runqemu.py test file
#
# Copyright (c) 2017 Wind River Systems, Inc.
#
# SPDX-License-Identifier: MIT
#

from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, runqemu

class GenericEFITest(OESelftestTestCase):
    """EFI booting test class"""
    image = "core-image-minimal"

    # TODO limit to x86
    def test_boot_efi(self):
        """Test generic boot partition with qemu"""
        self.write_config(self, """
EFI_PROVIDER = "systemd-boot"
IMAGE_FSTYPES:pn-%s:append = " wic"
MACHINE_FEATURES:append = " efi"
WKS_FILE = "efi-bootdisk.wks.in"
IMAGE_INSTALL:append = " grub-efi systemd-boot kernel-image"
"""
% (self.image))

        bitbake("ovmf")
        bitbake(self.image)

        cmd = "%s %s" % (self.cmd_common, self.machine)
        with runqemu(self.image, ssh=False, runqemuparams='nographic serial wic ovmf') as qemu:
            self.assertTrue(qemu.runner.logged, "Failed: %s" % cmd)
