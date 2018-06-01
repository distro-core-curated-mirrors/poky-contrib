SUMMARY = "Perl scripting language"
HOMEPAGE = "http://www.perl.org/"
SECTION = "devel"
LICENSE = "Artistic-1.0 | GPL-1.0+"
LIC_FILES_CHKSUM = "file://Copying;md5=5b122a36d0f6dc55279a0ebc69f3c60b \
                    file://Artistic;md5=2e6fd2475335af892494fe1f7327baf3"


SRC_URI = "https://www.cpan.org/src/5.0/perl-${PV}.tar.gz;name=perl \
           https://github.com/arsv/perl-cross/releases/download/1.1.9/perl-cross-1.1.9.tar.gz;name=perl-cross \
           file://0001-configure_tool.sh-do-not-quote-the-argument-to-comma.patch \
           file://0001-ExtUtils-MakeMaker-add-LDFLAGS-when-linking-binary-m.patch \
           file://0001-Somehow-this-module-breaks-through-the-perl-wrapper-.patch \
           "

SRC_URI[perl.md5sum] = "dc0fea097f3992a8cd53f8ac0810d523"
SRC_URI[perl.sha256sum] = "572f9cea625d6062f8a63b5cee9d3ee840800a001d2bb201a41b9a177ab7f70d"
SRC_URI[perl-cross.md5sum] = "af8f6f288019e670f0fdf7de4f28cd12"
SRC_URI[perl-cross.sha256sum] = "0bbb450e48d07e7fdf867d578b1780ac8f0e8dc284d52301dac4d763b42f6041"

S = "${WORKDIR}/perl-${PV}"

inherit upstream-version-is-even

do_patch_prepend() {
    bb.build.exec_func('do_copy_perlcross', d)
}

do_copy_perlcross() {
    cp -rf ${WORKDIR}/perl-cross*/* ${S}
}

do_configure_class-target() {
    ./configure --prefix=${prefix} --target=${TARGET_SYS}
}

do_configure_class-nativesdk() {
    ./configure --prefix=${prefix} --target=${TARGET_SYS}
}

do_configure() {
    ./configure --prefix=${prefix}
}

do_compile() {
    oe_runmake miniperl
    oe_runmake config-pm
    oe_runmake
}

do_install() {
    oe_runmake 'DESTDIR=${D}' install
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

