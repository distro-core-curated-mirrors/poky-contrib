DESCRIPTION = "SystemTap - script-directed dynamic tracing and performance analysis tool for Linux"

require systemtap_git.inc

DEPENDS = "elfutils sqlite3 systemtap-native"
<<<<<<< HEAD
DEPENDS_class-native = "elfutils-native sqlite3-native gettext-native"
DEPENDS_class-nativesdk = "nativesdk-elfutils nativesdk-sqlite3 nativesdk-gettext"

RDEPENDS_${PN} += "python bash"
RDEPENDS_${PN}_class-native += "python-native"
RDEPENDS_${PN}_class-nativesdk += "python-native"

EXTRA_OECONF += "--with-libelf=${STAGING_DIR_TARGET} --without-rpm \
            --without-nss --without-avahi --without-dyninst \
            --disable-server --disable-grapher \
            ac_cv_prog_have_javac=no \
            ac_cv_prog_have_jar=no "

STAP_DOCS ?= "--disable-docs --disable-publican --disable-refdocs"

EXTRA_OECONF += "${STAP_DOCS} "

inherit autotools gettext pkgconfig

=======
DEPENDS_virtclass-native = "elfutils-native sqlite3-native gettext-native"
DEPENDS_virtclass-nativesdk = "nativesdk-elfutils nativesdk-sqlite3 nativesdk-gettext"

PR = "r0"

export CC_FOR_BUILD = "${BUILD_CC}"
export CFLAGS_FOR_BUILD = "${BUILD_CFLAGS}"
export LDFLAGS_FOR_BUILD = "${BUILD_LDFLAGS}"

EXTRA_OECONF += "--with-libelf=${STAGING_DIR_TARGET} --without-rpm \
            --without-nss --without-avahi \
            --disable-server --disable-grapher "

STAP_DOCS ?= "--disable-docs --disable-publican --disable-refdocs"

EXTRA_OECONF += "${STAP_DOCS} "

inherit autotools gettext

>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
BBCLASSEXTEND = "native nativesdk"

FILES_${PN}-dbg += "${libexecdir}/systemtap/.debug"
