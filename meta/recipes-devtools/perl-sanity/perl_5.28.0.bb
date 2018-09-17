SUMMARY = "Perl scripting language"
HOMEPAGE = "http://www.perl.org/"
SECTION = "devel"
LICENSE = "Artistic-1.0 | GPL-1.0+"
LIC_FILES_CHKSUM = "file://Copying;md5=5b122a36d0f6dc55279a0ebc69f3c60b \
                    file://Artistic;md5=71a4d5d9acc18c0952a6df2218bb68da \
                    "


SRC_URI = "https://www.cpan.org/src/5.0/perl-${PV}.tar.gz;name=perl \
           https://github.com/arsv/perl-cross/releases/download/1.2/perl-cross-1.2.tar.gz;name=perl-cross \
           file://0001-configure_tool.sh-do-not-quote-the-argument-to-comma.patch \
           file://0001-ExtUtils-MakeMaker-add-LDFLAGS-when-linking-binary-m.patch \
           file://0001-Somehow-this-module-breaks-through-the-perl-wrapper-.patch \
           "

SRC_URI[perl.md5sum] = "c7c63781745e280e08401a306a83bfb8"
SRC_URI[perl.sha256sum] = "7e929f64d4cb0e9d1159d4a59fc89394e27fa1f7004d0836ca0d514685406ea8"
SRC_URI[perl-cross.md5sum] = "2d702f8fa1dba84d0a62de30e8a9c263"
SRC_URI[perl-cross.sha256sum] = "599077beb86af5e6097da8922a84474a5484f61475d2899eae0f8634e9619109"

S = "${WORKDIR}/perl-${PV}"

inherit upstream-version-is-even

do_patch_prepend() {
    bb.build.exec_func('do_copy_perlcross', d)
}

do_copy_perlcross() {
    cp -rf ${WORKDIR}/perl-cross*/* ${S}
}

do_configure_class-target() {
    ./configure --prefix=${prefix} --target=${TARGET_SYS} -Dvendorprefix=${prefix}
}

do_configure_class-nativesdk() {
    ./configure --prefix=${prefix} --target=${TARGET_SYS} -Dvendorprefix=${prefix}
}

do_configure() {
    ./configure --prefix=${prefix} -Dvendorprefix=${prefix}
}

do_compile() {
    oe_runmake miniperl
    oe_runmake config-pm
    oe_runmake
}

do_install() {
    oe_runmake 'DESTDIR=${D}' install

    install -d ${D}${libdir}/perl
    install -d ${D}${libdir}/perl/${PV}/
    install -d ${D}${libdir}/perl/${PV}/ExtUtils/

    # Save native config
    install config.sh ${D}${libdir}/perl
    install lib/Config.pm ${D}${libdir}/perl/${PV}/
    install lib/ExtUtils/typemap ${D}${libdir}/perl/${PV}/ExtUtils/
}

do_install_append_class-native () {
    # Those wrappers mean that perl installed from sstate (which may change
    # path location) works and that in the nativesdk case, the SDK can be
    # installed to a different location from the one it was built for.
    create_wrapper ${D}${bindir}/perl PERL5LIB='$PERL5LIB:${STAGING_LIBDIR}/perl5/site_perl/${PV}:${STAGING_LIBDIR}/perl5/vendor_perl/${PV}:${STAGING_LIBDIR}/perl5/${PV}'
    create_wrapper ${D}${bindir}/perl${PV} PERL5LIB='$PERL5LIB:${STAGING_LIBDIR}/perl5/site_perl/${PV}:${STAGING_LIBDIR}/perl5/vendor_perl/${PV}:${STAGING_LIBDIR}/perl5/${PV}'
}

require perl-ptest.inc

FILES_${PN}_append = " ${libdir}/perl5/site_perl \
               ${libdir}/perl5/${PV}/Config.pm \
               ${libdir}/perl5/${PV}/strict.pm \
               ${libdir}/perl5/${PV}/warnings.pm \
               ${libdir}/perl5/${PV}/warnings \
               ${libdir}/perl5/${PV}/vars.pm \
               "

FILES_${PN}-staticdev_append = " ${libdir}/perl5/${PV}/*/CORE/libperl.a"

FILES_${PN}-dev_append = " ${libdir}/perl5/${PV}/*/CORE"

FILES_${PN}-doc_append = " ${libdir}/perl5/${PV}/Unicode/Collate/*.txt \
                           ${libdir}/perl5/${PV}/*/.packlist \
                           ${libdir}/perl5/${PV}/ExtUtils/MANIFEST.SKIP \
                           ${libdir}/perl5/${PV}/ExtUtils/xsubpp \
                           ${libdir}/perl5/${PV}/ExtUtils/typemap \
                           ${libdir}/perl5/${PV}/Encode/encode.h \
                         "

PACKAGES_append = " ${PN}-pod"

FILES_${PN}-pod = "${libdir}/perl5/${PV}/pod \
                   ${libdir}/perl5/${PV}/*.pod \
                   ${libdir}/perl5/${PV}/*/*.pod \
                   ${libdir}/perl5/${PV}/*/*/*.pod \ 
                   ${libdir}/perl5/${PV}/*/*/*/*.pod \ 
                  "
RDEPENDS_${PN}-pod += "perl"

PACKAGES_append = " ${PN}-module-cpan ${PN}-module-unicore"

FILES_${PN}-module-cpan += "${libdir}/perl5/${PV}/CPAN \
                          "
FILES_${PN}-module-unicore += "${libdir}/perl5/${PV}/unicore"

# Create a perl-modules package recommending all the other perl
# packages (actually the non modules packages and not created too)
ALLOW_EMPTY_${PN}-modules = "1"
PACKAGES_append = " ${PN}-modules "

PACKAGESPLITFUNCS_prepend = "split_perl_packages "

python split_perl_packages () {
    libdir = d.expand('${libdir}/perl5/${PV}')
    do_split_packages(d, libdir, '.*/auto/([^.]*)/[^/]*\.(so|ld|ix|al)', '${PN}-module-%s', 'perl module %s', recursive=True, match_path=True, prepend=False)
    do_split_packages(d, libdir, '.*linux/([^\/]*)\.pm', '${PN}-module-%s', 'perl module %s', recursive=True, allow_dirs=False, match_path=True, prepend=False)
    do_split_packages(d, libdir, 'Module/([^\/]*)\.pm', '${PN}-module-%s', 'perl module %s', recursive=True, allow_dirs=False, match_path=True, prepend=False)
    do_split_packages(d, libdir, 'Module/([^\/]*)/.*', '${PN}-module-%s', 'perl module %s', recursive=True, allow_dirs=False, match_path=True, prepend=False)
    do_split_packages(d, libdir, '.*linux/([^\/].*)\.(pm|pl|e2x)', '${PN}-module-%s', 'perl module %s', recursive=True, allow_dirs=False, match_path=True, prepend=False)
    do_split_packages(d, libdir, '(^(?!(CPAN\/|CPANPLUS\/|Module\/|unicore\/)[^\/]).*)\.(pm|pl|e2x)', '${PN}-module-%s', 'perl module %s', recursive=True, allow_dirs=False, match_path=True, prepend=False)

    # perl-modules should recommend every perl module, and only the
    # modules. Don't attempt to use the result of do_split_packages() as some
    # modules are manually split (eg. perl-module-unicore).
    packages = filter(lambda p: '${PN}-module-' in p, d.getVar('PACKAGES').split())
    d.setVar(d.expand("RRECOMMENDS_${PN}-modules"), ' '.join(packages))
}

PACKAGES_DYNAMIC_class-target += "^${PN}-module-.*"
PACKAGES_DYNAMIC_class-nativesdk += "^${PN}-module-.*"

PACKAGES_append = " ${PN}-misc"
RDEPENDS_${PN}-misc += "perl perl-modules"

BBCLASSEXTEND = "native nativesdk"
