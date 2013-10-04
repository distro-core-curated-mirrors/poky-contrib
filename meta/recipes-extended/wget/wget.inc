DESCRIPTION = "A console URL download utility featuring HTTP, FTP, and more."
SECTION = "console/network"
LICENSE = "GPLv3"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"
<<<<<<< HEAD
DEPENDS = "openssl zlib"
=======
DEPENDS = "openssl"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

INC_PR = "r16"

inherit autotools gettext update-alternatives

EXTRA_OECONF = "--with-libc --enable-ipv6 --with-libssl-prefix=${STAGING_DIR_HOST} \
<<<<<<< HEAD
                --with-ssl=openssl --disable-rpath --disable-iri \
                ac_cv_header_uuid_uuid_h=no"
=======
                --with-ssl=openssl --disable-rpath --disable-iri"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

ALTERNATIVE_${PN} = "wget"
ALTERNATIVE_PRIORITY = "100"
