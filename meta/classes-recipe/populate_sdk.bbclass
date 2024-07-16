#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

# The majority of populate_sdk is located in populate_sdk_base
# This chunk simply facilitates compatibility with SDK only recipes.

# Handle inherits of any of the image classes we need
# This is required to handle testsdk loading
SDKCLASSES = "${IMAGE_CLASSES}"

# Some test cases may attempt to access IMAGE_FEATURES
IMAGE_FEATURES ??= ""
IMAGE_FEATURES[type] ??= "list"

inherit populate_sdk_base

inherit_defer ${SDKCLASSES}

addtask populate_sdk after do_install before do_build

