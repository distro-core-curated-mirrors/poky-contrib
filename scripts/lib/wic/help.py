# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
# Copyright (c) 2013, Intel Corporation.
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# DESCRIPTION
# This module implements some basic help invocation functions along
# with the bulk of the help topic text for the OE Core Image Tools.
#
# AUTHORS
# Tom Zanussi <tom.zanussi (at] linux.intel.com>
#

import subprocess
import logging

from wic.pluginbase import PluginMgr, PLUGIN_TYPES

# ##
# wic help and usage strings
##

wic_create_short_description = """
Create a new OpenEmbedded image.
"""

wic_rm_short_description = """
Remove files or directories from the vfat or ext* partitions.
"""

wic_write_short_description = """
Write an image to a device.
"""

wic_cp_short_description = """
Copy files and directories to the vfat or ext* partitions.
"""

wic_ls_short_description = """
Lists either partitions of the image or directory contents
of vfat or ext* partitions."""
wic_help_short_description = """
sss
"""
wic_list_short_description = """
List available canned images and source plugins
"""

wic_create_description = """
This command creates an OpenEmbedded image based on the 'OE
kickstart commands' found in the <wks file>.

In order to do this, wic needs to know the locations of the
various build artifacts required to build the image.

Users can explicitly specify the build artifact locations using
the -r, -b, -k, and -n options.  See below for details on where
the corresponding artifacts are typically found in a normal
OpenEmbedded build.

Alternatively, users can use the -e option to have 'wic' determine
those locations for a given image.  If the -e option is used, the
user needs to have set the appropriate MACHINE variable in
local.conf, and have sourced the build environment.

The -s option is used to skip the build check.  The build check is
a simple sanity check used to determine whether the user has
sourced the build environment so that the -e option can operate
correctly.  If the user has specified the build artifact locations
explicitly, 'wic' assumes the user knows what he or she is doing
and skips the build check.

When 'wic -e' is used, the locations for the build artifacts
values are determined by 'wic -e' from the output of the 'bitbake
-e' command given an image name e.g. 'core-image-minimal' and a
given machine set in local.conf.  In that case, the image is
created as if the following 'bitbake -e' variables were used:

-r:        IMAGE_ROOTFS
-k:        STAGING_KERNEL_DIR
-n:        STAGING_DIR_NATIVE
-b:        empty (plugin-specific handlers must determine this)

If 'wic -e' is not used, the user needs to select the appropriate
value for -b (as well as -r, -k, and -n).

Here's an example that doesn't take the easy way out and manually
specifies each build artifact, along with a non-canned .wks file,
and also uses the -o option to have wic create the output
somewhere other than the default /var/tmp/wic:

  $ wic create ./test.wks -o ./out --rootfs-dir
  tmp/work/qemux86_64-poky-linux/core-image-minimal/1.0-r0/rootfs
  --bootimg-dir tmp/sysroots/qemux86-64/usr/share
  --kernel-dir tmp/deploy/images/qemux86-64
  --native-sysroot tmp/sysroots/x86_64-linux
"""


wic_list_description = """
This command enumerates the set of available canned images as well
as help for those images.  It also can be used to list available
source plugins.

The first form enumerates all the available 'canned' images.
These are actually just the set of .wks files that have been moved
into the /scripts/lib/wic/canned-wks directory).

The second form lists the detailed help information for a specific
'canned' image.

The third form enumerates all the available --sources (source
plugins).  The contents of a given partition are driven by code
defined in 'source plugins'.  Users specify a specific plugin via
the --source parameter of the partition .wks command.  Normally
this is the 'rootfs' plugin but can be any of the more specialized
sources listed by the 'list source-plugins' command.  Users can
also add their own source plugins - see 'wic help plugins' for
details.
"""


wic_ls_description = """
This command lists either partitions of the image or directory contents
of vfat or ext* partitions.

The first form lists partitions of the image.
For example:
    $ wic ls tmp/deploy/images/qemux86-64/core-image-minimal-qemux86-64.wic
    Num     Start        End          Size      Fstype
    1        1048576     24438783     23390208  fat16
    2       25165824     50315263     25149440  ext4

The second form lists directory contents of the first partition:

    $ wic ls tmp/deploy/images/qemux86-64/core-image-minimal-qemux86-64.wic:1/EFI/boot/
    Volume in drive : is boot
     Volume Serial Number is 2DF2-5F02
    Directory for ::/EFI/boot

    .            <DIR>     2017-05-11  10:54
    ..           <DIR>     2017-05-11  10:54
    grub     cfg       679 2017-05-11  10:54
    bootx64  efi    571392 2017-05-11  10:54
            4 files             572 071 bytes
                             15 818 752 bytes free

"""

wic_cp_description = """
This command copies files and directories to the vfat or ext* partition of
the partitioned image.

Copies file or directory to the specified directory
on the partition:
   $ wic cp test tmp/deploy/images/qemux86-64/core-image-minimal-qemux86-64.wic:1/efi/
"""


wic_rm_description = """
This command removes files or directories from the vfat or ext* partition of the
partitioned image: wic rm <wic image>:<partition><path> 

$wic rm ./tmp/deploy/images/qemux86-64/core-image-minimal-qemux86-64.wic:1/libutil.c32 

"""

wic_write_description = """
This command writes an image to a target device (USB stick, SD card etc)

    $ wic write ./tmp/deploy/images/qemux86-64/core-image-minimal-qemux86-64.wic /dev/sdb

The --expand option is used to resize image partitions.
--expand auto expands partitions to occupy all free space available on the target device.
It's also possible to specify expansion rules in a format
<partition>:<size>[-<partition>:<size>...] for one or more partitions.
Specifying size 0 will keep partition unmodified.
Note: Resizing boot partition can result in non-bootable image for non-EFI images. It is
recommended to use size 0 for boot partition to keep image bootable.

"""
