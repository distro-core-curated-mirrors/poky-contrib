SUMMARY = "A GNU tool that produce shell scripts to automatically configure software"
DESCRIPTION = "Autoconf is an extensible package of M4 macros that produce shell scripts to automatically \ 
configure software source code packages. Autoconf creates a configuration script for a package from a template \
file that lists the operating system features that the package can use, in the form of M4 macro calls."
LICENSE = "GPL-3.0-or-later"
HOMEPAGE = "http://www.gnu.org/software/autoconf/"
SECTION = "devel"
DEPENDS = "m4-native autoconf-native automake-native gnu-config-native help2man-native"
DEPENDS:remove:class-native = "autoconf-native automake-native help2man-native"

LIC_FILES_CHKSUM = "file://COPYING;md5=cc3f3a7596cb558bbd9eb7fbaa3ef16c \
		    file://COPYINGv3;md5=1ebbd3e34237af26da5dc08a4e440464"

SRC_URI = " \
           https://alpha.gnu.org/gnu/autoconf/autoconf-2.72c.tar.gz \
           file://program_prefix.patch \
           file://autoreconf-exclude.patch \
           file://remove-usr-local-lib-from-m4.patch \
           file://preferbash.patch \
           file://autotest-automake-result-format.patch \
           file://man-host-perl.patch \
           file://0004-Cater-to-programs-misusing-AC_EGREP_HEADER.patch \
           file://0007-Support-underquoted-callers-better.patch \
           file://0001-AC_XENIX_DIR-Rewrite-using-AC_CANONICAL_HOST.patch \
           file://0002-AC_TYPE_UID_T-Rewrite-using-AC_CHECK_TYPE.patch \
           file://0003-Make-AC_PROG_GCC_TRADITIONAL-a-compatibility-alias-f.patch \
           file://0004-Overhaul-AC_TYPE_GETGROUPS-and-AC_FUNC_GETGROUPS.patch \
           file://0005-Fold-AC_C_STRINGIZE-into-AC_PROG_CC.patch \
           file://0006-Remove-the-last-few-internal-uses-of-AC_EGREP_CPP.patch \
           file://0007-Support-circa-early-2022-Gnulib.patch \
           "
SRC_URI:append:class-native = " file://no-man.patch"

SRC_URI[sha256sum] = "21b64169c820c6cdf27fc981ca9c2fb615546e5dead92bccf8d92d0784cdd364"

RDEPENDS:${PN} = "m4 gnu-config \
		  perl \
		  perl-module-bytes \
		  perl-module-carp \
		  perl-module-constant \
		  perl-module-data-dumper \
		  perl-module-errno \
		  perl-module-exporter \
		  perl-module-file-basename \
		  perl-module-file-compare \
		  perl-module-file-copy \
		  perl-module-file-find \
		  perl-module-file-glob \
		  perl-module-file-path \
		  perl-module-file-spec \
		  perl-module-file-spec-unix \
		  perl-module-file-stat \
                  perl-module-file-temp \
		  perl-module-getopt-long \
		  perl-module-io-file \
                  perl-module-list-util \
		  perl-module-overloading \
		  perl-module-posix \
                  perl-module-scalar-util \
		  perl-module-symbol \
		  perl-module-thread-queue \
		  perl-module-threads \
		 "
RDEPENDS:${PN}:class-native = "m4-native gnu-config-native hostperl-runtime-native"

inherit autotools texinfo

PERL = "${USRBINPATH}/perl"
PERL:class-native = "/usr/bin/env perl"
PERL:class-nativesdk = "/usr/bin/env perl"

CACHED_CONFIGUREVARS += "ac_cv_path_PERL='${PERL}'"

EXTRA_OECONF += "ac_cv_path_M4=m4 ac_cv_prog_TEST_EMACS=no"

# As autoconf installs its own config.* files, ensure that they're always up to date.
update_gnu_config() {
	install -m 0755 ${STAGING_DATADIR_NATIVE}/gnu-config/config.guess ${S}/build-aux
	install -m 0755 ${STAGING_DATADIR_NATIVE}/gnu-config/config.sub ${S}/build-aux
}
do_configure[prefuncs] += "update_gnu_config"

do_configure:class-native() {
	oe_runconf
}

do_install:append() {
    rm -rf ${D}${datadir}/emacs
}

BBCLASSEXTEND = "native nativesdk"
