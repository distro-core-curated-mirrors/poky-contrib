SUMMARY = "Tools to add packaging metadata to ELF files"
HOMEPAGE = "https://systemd.io/ELF_PACKAGE_METADATA/"

LICENSE = "CC0-1.0"
LIC_FILES_CHKSUM = "file://dlopen-notes.py;beginline=2;endline=2;md5=f93d9e18b74c6270d45a8478fc9eebc8"

SRC_URI = "git://github.com/systemd/package-notes;protocol=https;branch=main"
SRCREV = "422c3738b0a0c5f220fd5cd4f9e111dc77a79918"

S = "${WORKDIR}/git"

do_install() {
    # TODO upstream hardcodes bindir
    install -d ${D}${bindir}
    install -m 755 -D ${S}/dlopen-notes.py ${D}${bindir}
}

RDEPENDS:${PN} = "python3-pyelftools"

BBCLASSEXTEND = "native"
