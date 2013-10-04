#
# base machine settings for ia32-architecture BSPs
#

#
# common settings for Intel-based machines
#
MACHINE_FEATURES += "screen keyboard pci usbhost ext2 ext3 x86 \
                     acpi serial usbgadget alsa"

MACHINE_EXTRA_RRECOMMENDS += "kernel-modules eee-acpi-scripts"
<<<<<<< HEAD
=======
MACHINE_ESSENTIAL_EXTRA_RDEPENDS += "grub"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

IMAGE_FSTYPES += "ext3 cpio.gz live"

KERNEL_IMAGETYPE ?= "bzImage"

SERIAL_CONSOLE ?= "115200 ttyS0"

#
# kernel-related variables
#
PREFERRED_PROVIDER_virtual/kernel ??= "linux-yocto"
PREFERRED_VERSION_linux-yocto ??= "3.0%"

#
# XSERVER subcomponents, used to build the XSERVER variable
#
XSERVER_IA32_BASE = "xserver-xorg \
           xf86-input-mouse \
           xf86-input-keyboard \
           xf86-input-evdev \
           xf86-input-synaptics \
           "

<<<<<<< HEAD
XSERVER_IA32_EXT = " \
           ${@base_contains('DISTRO_FEATURES', 'opengl', 'xserver-xorg-extension-glx', '', d)} \
=======
XSERVER_IA32_EXT = "xserver-xorg-extension-dri \
           xserver-xorg-extension-dri2 \
           xserver-xorg-extension-glx \
           xserver-xorg-extension-extmod \
           xserver-xorg-extension-dbe \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
           xserver-xorg-module-libint10 \
           "

XSERVER_IA32_I915 = "xf86-video-intel \
<<<<<<< HEAD
           ${@base_contains('DISTRO_FEATURES', 'opengl', 'mesa-driver-i915', '', d)} \
           "

XSERVER_IA32_I965 = "xf86-video-intel \
           ${@base_contains('DISTRO_FEATURES', 'opengl', 'mesa-driver-i965', '', d)} \
           "

XSERVER_IA32_VESA = "xf86-video-vesa"

XSERVER_IA32_FBDEV = "xf86-video-fbdev"

XSERVER_IA32_MODESETTING = "xf86-video-modesetting"
=======
           mesa-dri-driver-i915 \
           "

XSERVER_IA32_I965 = "xf86-video-intel \
           mesa-dri-driver-i965 \
           "

XSERVER_IA32_VESA = "xf86-video-vesa"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
