inherit ${@bb.utils.contains('DISTRO_FEATURES', 'selinux', 'enable-audit', '', d)}
inherit ${@bb.utils.contains('DISTRO_FEATURES', 'selinux', 'enable-selinux', '', d)}
