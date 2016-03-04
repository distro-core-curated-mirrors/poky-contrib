#
# This include points at uninative tarballs generated and maintained
# by the Yocto Project. These file can be included by distros if they
# want to use/maintain a unified sstate feed for native/cross artefacts
# rather than the feeds having native/cross artefacts which are specific
# to the distro running on the build machine.
#

UNINATIVE_URL = "http://downloads.yoctoproject.org/releases/uninative/0.9/"
UNINATIVE_CHECKSUM[i686] = "d74d476bfcf9b82d8e8befb98b87068b"
UNINATIVE_CHECKSUM[x86_64] = "2b727b6a8e47999ff58da7d7db16fc2f"
