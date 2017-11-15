inherit deploy

# Extract UUID from ${ROOTFS}, which must have been built
# by the time that this function gets called. Only works
# on ext file systems and depends on tune2fs.
def get_rootfs_uuid(d):
    import os
    import uuid
    deploydir = d.getVar('DEPLOY_DIR_IMAGE')
    bootfs_uuid_file = deploydir + "/bootfs-uuid"
    uuid_str = "deadbeef-dead-beef-dead-beefdeadbeef"
    if d.getVar('BUILD_REPRODUCIBLE_BINARIES', True) != "1":
        if os.path.exists(bootfs_uuid_file):
            with open(bootfs_uuid_file, "r+") as file:
                uuid_str = file.read()
        else:
            # deploydir might not exist yet...creating it here could be bad?
            if not os.path.exists(deploydir):
                os.makedirs(deploydir)
            uuid_str = str(uuid.uuid4())
            with open(bootfs_uuid_file, "w") as file:
                file.write(uuid_str)
    return uuid_str

# Replace the special <<uuid-of-rootfs>> inside a string (like the
# root= APPEND string in a syslinux.cfg or systemd-boot entry) with the
# actual UUID of the rootfs. Does nothing if the special string
# is not used.
def replace_rootfs_uuid(d, string):
    UUID_PLACEHOLDER = '<<uuid-of-rootfs>>'
    if UUID_PLACEHOLDER in string:
        uuid = d.getVar('DISK_SIGNATURE_UUID', True)
        string = string.replace(UUID_PLACEHOLDER, uuid)
    return string

DISK_SIGNATURE_UUID ?= "${@get_rootfs_uuid(d)}"
