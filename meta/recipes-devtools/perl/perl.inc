SUMMARY = "Perl scripting language"
HOMEPAGE = "http://www.perl.org/"
SECTION = "devel"
LICENSE = "Artistic-1.0 | GPL-1.0+"
LIC_FILES_CHKSUM = "file://Copying;md5=5b122a36d0f6dc55279a0ebc69f3c60b \
		    file://Artistic;md5=2e6fd2475335af892494fe1f7327baf3"

SRC_URI = "http://www.cpan.org/src/5.0/${BP}.tar.xz"

SRC_URI[md5sum] = "59456ae4bd4b06cb6e57cb19a3b2d349"
SRC_URI[sha256sum] = "a9a37c0860380ecd7b23aa06d61c20fc5bc6d95198029f3684c44a9d7e2952f2"

inherit upstream-version-is-even
