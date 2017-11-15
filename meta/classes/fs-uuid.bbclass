inherit deploy

def get_rootfs_uuid(file_name, d):
    import os
    import uuid
    deploydir = d.getVar('DEPLOY_DIR_IMAGE')
    if not os.path.exists(deploydir):
        try:
            os.makedirs(deploydir)
        except FileExistsError:
            # We try to make sure it doesn't exist before creating, but it can race
            pass
    bootfs_uuid_file = os.path.join(deploydir, file_name)
    uuid_str = "deadbeef-dead-beef-dead-beefdeadbeef"
    if d.getVar('BUILD_REPRODUCIBLE_BINARIES', True) != "1":
        if os.path.exists(bootfs_uuid_file):
            with open(bootfs_uuid_file, "r+") as file:
                uuid_str = file.read()
        else:
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

DISK_SIGNATURE_UUID_FILE ?= "rootfs-uuid"
DISK_SIGNATURE_UUID ?= "${@get_rootfs_uuid(d.getVar('DISK_SIGNATURE_UUID_FILE'), d)}"

# useful if file-checksum is needed to trigger rebuilds
DISK_SIGNATURE_UUID_FULL_PATH ?= "${DEPLOY_DIR_IMAGE}/${DISK_SIGNATURE_UUID_FILE}"
