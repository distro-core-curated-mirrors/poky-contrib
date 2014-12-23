SRC_URI = "http://download.savannah.gnu.org/releases/avr-libc/avr-libc-1.8.1.tar.bz2"
LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://LICENSE;md5=8d91a8f153d3de715f67a5df0d841c43"

SRC_URI[md5sum] = "0caccead59eaaa61ac3f060ca3a803ef"
SRC_URI[sha256sum] = "c3062a481b6b2c6959dc708571c00b0e26301897ba21171ed92acd0af7c4a969"

inherit autotools

TOOLCHAIN_OPTIONS = ""

TARGET_CFLAGS = ""
TARGET_LDFLAGS = ""

export CC = "avr-gcc"
export AS = "avr-as"
export RANLIB = "avr-ranlib"
export AR = "avr-ar"

FILES_${PN} += "${exec_prefix}/avr"
INSANE_SKIP_${PN} = "arch staticdev"

python () {
    def replace(var, x, y):
        d.setVar(var, d.getVar(var, True).replace(d.expand(x),y))

    replace('CONFIGUREOPTS', '--host=${HOST_SYS}','--host=avr')
    replace('CONFIGUREOPTS', '--target=${TARGET_SYS}','--target=avr')
}


