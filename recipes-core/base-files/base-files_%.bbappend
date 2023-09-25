FILESEXTRAPATHS:prepend := "${THISDIR}/base-files:"

SRC_URI += "file://host.sh \
            file://guest.sh"

do_install:append() {
    install -m 0755 -d ${D}${bindir}
    install -m 0755 ${S}/host.sh ${D}${bindir}/host.sh
    install -m 0755 ${S}/guest.sh ${D}${bindir}/guest.sh
}


