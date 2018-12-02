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
           file://perl-configpm-switch.patch \
           file://errno_ver.diff \
           file://native-perlinc.patch \
           file://0001-perl-cross-add-LDFLAGS-when-linking-libperl.patch \
           file://perl-dynloader.patch \
           "

SRC_URI[perl.md5sum] = "c7c63781745e280e08401a306a83bfb8"
SRC_URI[perl.sha256sum] = "7e929f64d4cb0e9d1159d4a59fc89394e27fa1f7004d0836ca0d514685406ea8"
SRC_URI[perl-cross.md5sum] = "2d702f8fa1dba84d0a62de30e8a9c263"
SRC_URI[perl-cross.sha256sum] = "599077beb86af5e6097da8922a84474a5484f61475d2899eae0f8634e9619109"

S = "${WORKDIR}/perl-${PV}"

inherit upstream-version-is-even

do_unpack_append() {
    bb.build.exec_func('do_copy_perlcross', d)
}

do_copy_perlcross() {
    cp -rf ${WORKDIR}/perl-cross*/* ${S}
}

do_configure_class-target() {
    ./configure --prefix=${prefix} \
    --target=${TARGET_SYS} \
    -Duseshrplib \
    -Dsoname=libperl.so.5 \
    -Dvendorprefix=${prefix} \
    -Darchlibexp=${STAGING_LIBDIR}/perl5/${PV}/${TARGET_ARCH}-${TARGET_OS}
}

do_configure_class-nativesdk() {
    ./configure --prefix=${prefix} \
    --target=${TARGET_SYS} \
    -Duseshrplib \
    -Dsoname=libperl.so.5 \
    -Dvendorprefix=${prefix} 

}

do_configure_class-native() {
    ./configure --prefix=${prefix} \
    -Duseshrplib \
    -Dsoname=libperl.so.5 \
    -Dvendorprefix=${prefix}
}

do_compile() {
    oe_runmake miniperl
    oe_runmake config-pm
    oe_runmake
}

do_install() {
    oe_runmake 'DESTDIR=${D}' install

    install -d ${D}${libdir}/perl5
    install -d ${D}${libdir}/perl5/${PV}/
    install -d ${D}${libdir}/perl5/${PV}/ExtUtils/

    # Save native config
    install config.sh ${D}${libdir}/perl5
    install lib/Config.pm ${D}${libdir}/perl5/${PV}/
    install lib/ExtUtils/typemap ${D}${libdir}/perl5/${PV}/ExtUtils/

    # Fix up shared library
    rm ${D}/${libdir}/perl5/${PV}/${TARGET_ARCH}-${TARGET_OS}/CORE/libperl.so
    ln -sf ../../../../libperl.so.${PV} ${D}/${libdir}/perl5/${PV}/${TARGET_ARCH}-${TARGET_OS}/CORE/libperl.so
}

do_install_append_class-target() {
    # This is used to substitute target configuration when running native perl via perl-configpm-switch.patch
    ln -s Config_heavy.pl ${D}${libdir}/perl5/${PV}/${TARGET_ARCH}-${TARGET_OS}/Config_heavy-target.pl

}

do_install_append_class-native () {
    # Those wrappers mean that perl installed from sstate (which may change
    # path location) works and that in the nativesdk case, the SDK can be
    # installed to a different location from the one it was built for.
    create_wrapper ${D}${bindir}/perl PERL5LIB='$PERL5LIB:${STAGING_LIBDIR}/perl5/site_perl/${PV}:${STAGING_LIBDIR}/perl5/vendor_perl/${PV}:${STAGING_LIBDIR}/perl5/${PV}'
    create_wrapper ${D}${bindir}/perl${PV} PERL5LIB='$PERL5LIB:${STAGING_LIBDIR}/perl5/site_perl/${PV}:${STAGING_LIBDIR}/perl5/vendor_perl/${PV}:${STAGING_LIBDIR}/perl5/${PV}'
}

require perl-ptest.inc
require perl-rdepends_${PV}.inc

FILES_${PN}_append = " ${libdir}/libperl.so* \
               ${libdir}/perl5/site_perl \
               ${libdir}/perl5/${PV}/Config.pm \
               ${libdir}/perl5/${PV}/*/Config_heavy-target.pl \
               ${libdir}/perl5/config.sh \
               ${libdir}/perl5/${PV}/strict.pm \
               ${libdir}/perl5/${PV}/warnings.pm \
               ${libdir}/perl5/${PV}/warnings \
               ${libdir}/perl5/${PV}/vars.pm \
               ${libdir}/perl5/site_perl \
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

BBCLASSEXTEND = "native nativesdk"

SSTATE_SCAN_FILES += "*.pm *.pod *.h *.pl *.sh"

do_create_rdepends_inc() {
    cd ${WORKDIR}
    cat <<'EOPREAMBLE' > ${WORKDIR}/perl-rdepends.inc
# To create/update the perl-rdepends_${PV}.inc use this piece of ugly script (modified for your arch/paths etc):

#jiahongxu:5.20.0-r1$ pwd
#/home/jiahongxu/yocto/build-20140618-perl/tmp/work/i586-poky-linux/perl/5.20.0-r1

#1 cp -r packages-split packages-split.new && cd packages-split.new
#2 find . -name \*.pm | xargs sed -i '/^=head/,/^=cut/d'
#3 egrep -r "^\s*(\<use .*|\<require .*);?" perl-module-* --include="*.pm"
#| sed "s/\/.*\.pm: */ += /g;s/[\"\']//g;s/;.*/\"/g;s/+= .*\(require\|use\)\> */+= \"perl-module-/g;s/CPANPLUS::.*/cpanplus/g;s/CPAN::.*/cpan/g;s/::/-/g;s/ [^+\"].*//g;s/_/-/g;s/\.pl\"$/\"/;s/\"\?\$/\"/;s/(//;" | tr [:upper:] [:lower:]
#| awk '{if ($3 != "\x22"$1"\x22"){ print $0}}'
#| grep -v -e "\-vms\-" -e module-5 -e "^$" -e "\\$" -e your -e tk -e autoperl -e html -e http -e parse-cpan -e perl-ostype -e ndbm-file -e module-mac -e fcgi -e lwp -e dbd -e dbix
#| sort -u
#| sed 's/^/RDEPENDS_/;s/perl-module-/${PN}-module-/g;s/module-\(module-\)/\1/g;s/\(module-load\)-conditional/\1/g;s/encode-configlocal/&-pm/;'
#| egrep -wv '=>|module-a|module-apache.?|module-apr|module-authen-sasl|module-b-asmdata|module-convert-ebcdic|module-devel-size|module-digest-perl-md5|module-dumpvalue|module-extutils-constant-aaargh56hash|module-extutils-xssymset|module-file-bsdglob|module-for|module-it|module-io-string|module-ipc-system-simple|module-lexical|module-local-lib|metadata|module-modperl-util|module-pluggable-object|module-test-builder-io-scalar|module-text-unidecode|module-win32|objects\sload|syscall.ph|systeminfo.ph|%s' > /tmp/perl-rdepends

RDEPENDS_perl-misc += "perl perl-modules"
RDEPENDS_${PN}-pod += "perl"

# Some additional dependencies that the above doesn't manage to figure out
RDEPENDS_${PN}-module-file-spec += "${PN}-module-file-spec-unix"
RDEPENDS_${PN}-module-math-bigint += "${PN}-module-math-bigint-calc"
RDEPENDS_${PN}-module-thread-queue += "${PN}-module-attributes"
RDEPENDS_${PN}-module-overload += "${PN}-module-overloading"

# Generated depends list beyond this line
EOPREAMBLE
    test -e packages-split.new && rm -rf packages-split.new
    cp -r packages-split packages-split.new && cd packages-split.new
    find . -name \*.pm | xargs sed -i '/^=head/,/^=cut/d'
    egrep -r "^\s*(\<use .*|\<require .*);?" perl-module-* --include="*.pm" | \
    sed "s/\/.*\.pm: */ += /g;s/[\"\']//g;s/;.*/\"/g;s/+= .*\(require\|use\)\> */+= \"perl-module-/g;s/CPANPLUS::.*/cpanplus/g;s/CPAN::.*/cpan/g;s/::/-/g;s/ [^+\"].*//g;s/_/-/g;s/\.pl\"$/\"/;s/\"\?\$/\"/;s/(//;" | tr [:upper:] [:lower:] | \
    awk '{if ($3 != "\x22"$1"\x22"){ print $0}}'| \
    grep -v -e "\-vms\-" -e module-5 -e "^$" -e "\\$" -e your -e tk -e autoperl -e html -e http -e parse-cpan -e perl-ostype -e ndbm-file -e module-mac -e fcgi -e lwp -e dbd -e dbix | \
    sort -u | \
    sed 's/^/RDEPENDS_/;s/perl-module-/${PN}-module-/g;s/module-\(module-\)/\1/g;s/\(module-load\)-conditional/\1/g;s/encode-configlocal/&-pm/;' | \
    egrep -wv '=>|module-a|module-apache.?|module-apr|module-authen-sasl|module-b-asmdata|module-convert-ebcdic|module-devel-size|module-digest-perl-md5|module-dumpvalue|module-extutils-constant-aaargh56hash|module-extutils-xssymset|module-file-bsdglob|module-for|module-it|module-io-socket-inet6|module-io-socket-ssl|module-io-string|module-ipc-system-simple|module-lexical|module-local-lib|metadata|module-modperl-util|module-pluggable-object|module-test-builder-io-scalar|module-test2|module-text-unidecode|module-unicore|module-win32|objects\sload|syscall.ph|systeminfo.ph|%s' | \
    egrep -wv '=>|module-algorithm-diff|module-carp|module-c<extutils-mm-unix>|module-encode-hanextra|module-extutils-makemaker-version-regex|module-file-spec|module-io-compress-lzma|module-locale-maketext-lexicon|module-log-agent|module-meta-notation|module-net-localcfg|module-net-ping-external|module-b-deparse|module-scalar-util|module-some-module|module-symbol|module-uri|module-win32api-file' >> ${WORKDIR}/perl-rdepends.inc
    cp ${WORKDIR}/perl-rdepends.inc ${THISDIR}/perl-rdepends_${PV}.inc
}

# bitbake perl -c create_rdepends_inc
addtask do_create_rdepends_inc

# Make sure we have native python ready when we create a new manifest
do_create_rdepends_inc[depends] += "python3:do_prepare_recipe_sysroot"
do_create_rdepends_inc[depends] += "python3:do_package"
do_create_rdepends_inc[depends] += "python3:do_patch"
