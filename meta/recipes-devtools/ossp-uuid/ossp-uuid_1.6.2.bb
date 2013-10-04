SUMMARY = "Universally Unique Identifier (UUID) library" 
DESCRIPTION = "OSSP uuid is a ISO-C:1999 application programming interface \
(API) and corresponding command line interface (CLI) for the generation of \
DCE 1.1, ISO/IEC 11578:1996 and RFC 4122 compliant Universally Unique \
Identifier (UUID). It supports DCE 1.1 variant UUIDs of version 1 (time \
and node based), version 3 (name based, MD5), version 4 (random number \
based) and version 5 (name based, SHA-1)."
DESCRIPTION_uuid = "This package contains a tool to create Universally \
Unique Identifiers (UUID) from the command-line."

HOMEPAGE = "http://www.ossp.org/pkg/lib/uuid/"
SECTION = "libs"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://README;beginline=30;endline=55;md5=b394fadb039bbfca6ad9d9d769ee960e \
	   file://uuid_md5.c;beginline=1;endline=28;md5=9c1f4b2218546deae24c91be1dcf00dd"

<<<<<<< HEAD
PR = "r2"
=======
PR = "r1"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

SRC_URI = "ftp://ftp.ossp.org/pkg/lib/uuid/uuid-1.6.2.tar.gz \
	   file://0001-Change-library-name.patch \
	   file://0002-uuid-preserve-m-option-status-in-v-option-handling.patch \
	   file://0003-Fix-whatis-entries.patch \
	   file://0004-fix-data-uuid-from-string.patch \
	   file://uuid-libtool.patch \
	   file://uuid-nostrip.patch \
<<<<<<< HEAD
           file://install-pc.patch \
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
	  "
SRC_URI[md5sum] = "5db0d43a9022a6ebbbc25337ae28942f"
SRC_URI[sha256sum] = "11a615225baa5f8bb686824423f50e4427acd3f70d394765bdff32801f0fd5b0"

S = "${WORKDIR}/uuid-${PV}"

inherit autotools

EXTRA_OECONF = "--without-dce --without-cxx --without-perl --without-perl-compat --without-php --without-pgsql"
EXTRA_OECONF = "--includedir=${includedir}/ossp"

do_configure_prepend() {
<<<<<<< HEAD
  # This package has a completely custom aclocal.m4, which should be acinclude.m4.
  if [ ! -e ${S}/acinclude.m4 ]; then
    mv ${S}/aclocal.m4 ${S}/acinclude.m4
  fi

  rm -f ${S}/libtool.m4
=======
  # This package has a completely custom aclocal.m4
  # so we need to back it up and make it usable...
  if [ ! -e m4/ossp.m4 ]; then
    mkdir m4
    mv aclocal.m4 m4/ossp.m4
  fi

  rm -f libtool.m4
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
}

do_install_append() {
  mkdir -p  ${D}${includedir}/ossp
  mv ${D}${libdir}/pkgconfig/uuid.pc ${D}${libdir}/pkgconfig/ossp-uuid.pc
}

PACKAGES =+ "uuid"
FILES_uuid = "${bindir}/uuid"
FILES_${PN} = "${libdir}/libossp-uuid.so.16*"
FILES_${PN}-dev += "${bindir}/uuid-config"

BBCLASSEXTEND = "native"
