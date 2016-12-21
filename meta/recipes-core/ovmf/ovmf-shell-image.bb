# This needs to run before image.bbclass reads IMAGE_FSTYPES,
# which is guaranteed by the ordering of anonymous functions
# in a recipe.
python () {
    # Ignore customization of IMAGE_FSTYPES because
    # for this image recipe, only the .wic format
    # with a single vfat partition makes sense.
    d.setVar('IMAGE_FSTYPES', 'wic')
}
WKS_FILE = "ovmf/ovmf-shell-image.wks"

inherit image

# We want a minimal image with just ovmf-shell-efi
# unpacked in it. We avoid installing unnecessary
# stuff as much as possible, but some things still
# get through and need to be removed.
PACKAGE_INSTALL = "ovmf-shell-efi"
LINGUAS_INSTALL = ""
do_image () {
    rm -rf `ls -d ${IMAGE_ROOTFS}/* | grep -v efi`
}
