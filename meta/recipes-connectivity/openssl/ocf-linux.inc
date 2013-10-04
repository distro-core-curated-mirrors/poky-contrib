DESCRIPTION = "Install required headers to enable OCF Linux support"
LICENSE = "BSD"

<<<<<<< HEAD
LIC_FILES_CHKSUM = "file://README;md5=493ffe65655667614cf24567adf22f11"
=======
LIC_FILES_CHKSUM = "file://README;md5=b02a793c9b7893b4ce1f39f0b231ccd7"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
 
INC_PR = "r3"

SRC_URI = "http://sourceforge.net/projects/ocf-linux/files/ocf-linux/${PV}/ocf-linux-${PV}.tar.gz"

S = "${WORKDIR}/ocf-linux-${PV}"

# Need to unpack the the ocf-linux.tar.gz file contained inside the
# downloaded tarball
# Install the OCF Linux headers so that other packages such as openssl
# can find them.  The headers must be in a crypto directory according to
# the README file.
do_install() {
    cd ${S}
<<<<<<< HEAD
=======
    tar xzf ocf-linux.tar.gz
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    install -d ${D}${includedir}/crypto
    install -m 0644 ${S}/ocf/*.h ${D}${includedir}/crypto/
}

<<<<<<< HEAD
ALLOW_EMPTY_${PN} = "1"
=======
ALLOW_EMPTY = "1"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
BBCLASSEXTEND = "native nativesdk"
