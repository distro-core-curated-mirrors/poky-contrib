# This class contains common functions for overlayfs and its QA check,
# which is performed in ROOTFS_POSTPROCESS_COMMAND

# this function is based on https://github.com/systemd/systemd/blob/main/src/basic/unit-name.c
def escapeSystemdUnitName(path):
    escapeMap = {
        '/': '-',
        '-': "\\x2d",
        '\\': "\\x5d"
    }
    return "".join([escapeMap.get(c, c) for c in path.strip('/')])

def mountUnitName(unit):
    return escapeSystemdUnitName(unit) + '.mount'
