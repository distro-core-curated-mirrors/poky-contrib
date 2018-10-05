LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://COPYING;md5=f835cce8852481e4b2bbbdd23b5e47f3"

SRC_URI = "https://download.nfs-ganesha.org/2.7/2.7.0/ntirpc-1.7.0.tar.gz"
SRC_URI[md5sum] = "f025c6461e2b7a84cf00c493d3967e1e"
SRC_URI[sha256sum] = "61c72b481cd75945852df2f9ee5a6080e6f8cca7e57f4c7bc950f6cea0a7fbdb"

DEPENDS = "libnsl2"

inherit cmake

# Sort out the brain-dead cmake file
# (https://github.com/nfs-ganesha/ntirpc/issues/150)
do_install_append() {
    if [ "${prefix}/lib64" != "${libdir}" -a -d ${D}${prefix}/lib64 ]; then
        mv ${D}${prefix}/lib64 ${D}${libdir}
    fi
}

BBCLASSEXTEND = "native nativesdk"
