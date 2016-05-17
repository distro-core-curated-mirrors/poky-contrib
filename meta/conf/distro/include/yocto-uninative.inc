#
# This include points at uninative tarballs generated and maintained
# by the Yocto Project. These file can be included by distros if they
# want to use/maintain a unified sstate feed for native/cross artefacts
# rather than the feeds having native/cross artefacts which are specific
# to the distro running on the build machine.
#

UNINATIVE_URL = "http://downloads.yoctoproject.org/releases/uninative/1.0/"
UNINATIVE_CHECKSUM[i686] ?= "94a4693ec2df05d326e13dc1b613b7810ec7eeb5c9ce61d107c672cba49ac51a"
UNINATIVE_CHECKSUM[x86_64] ?= "d3f2153800a730f647d0e06b76be5321ca400a076ffcf90d5512b72098406a61"
