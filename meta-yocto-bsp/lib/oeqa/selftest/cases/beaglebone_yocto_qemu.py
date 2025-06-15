
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import runCmd, bitbake, runqemu, runqemu_check_taps
from oeqa.core.decorator import OETestTag


class BeagleboneYoctoQemuTests(OESelftestTestCase):

    @OETestTag("runqemu")
    def test_fit_image_initramfs_qemu(self):
        """
        Summary:     Verify building an image including a FIT image kernel and booting in Qemu works.
        Expected:    1. core-image-minimal including a FIT image in /boot gets built
                     2. Qemu can boot the zImage and initramfs with direct kernel boot
                        since Qemu does not support FIT images
        """

        config = """
DISTRO = "poky"
MACHINE = "beaglebone-yocto"
INITRAMFS_IMAGE = "core-image-initramfs-boot"
FIT_IMAGE_KERNEL = "1"
# Do not override kernel command line network configuration
BAD_RECOMMENDATIONS:append:pn-oe-selftest-image = " init-ifupdown"
"""
        self.write_config(config)
        if not runqemu_check_taps():
            self.skipTest('No tap devices found - you must set up tap devices with scripts/runqemu-gen-tapdevs before running this test')
        testimage = "oe-selftest-image"
        bitbake(testimage)
        # Boot the image
        with runqemu(testimage) as qemu:
            # Run a test command to see if it was installed properly
            sshargs = '-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
            result = runCmd('ssh %s root@%s %s' % (sshargs, qemu.ip, "ls -1 /boot"))
            self.logger.debug("ls -1 /boot: %s" % str(result.output))
            boot_files = result.output.splitlines()
            self.assertIn("fitImage", boot_files)
            self.assertNotIn("zImage", boot_files)
