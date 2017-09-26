EXTRA_OECONF += "--with-mode=thumb --with-fpu=vfpv3-d16 --with-arch=armv7-a --with-float=hard"
CONFIGUREOPTS := "${@d.getVar("CONFIGUREOPTS").replace("--target=${TARGET_SYS}", "--target=arm-linux-gnueabihf")}"
CONFIGUREOPTS := "${@d.getVar("CONFIGUREOPTS").replace("--host=${TARGET_SYS}", "--host=arm-linux-gnueabihf")}"
EXTRA_OECONF := "${@d.getVar("EXTRA_OECONF").replace("--program-prefix=${TARGET_SYS}-", "--program-prefix=arm-linux-gnueabihf-")}"
do_install := "${@d.getVar("do_install").replace("${TARGET_SYS}", "arm-linux-gnueabihf")}"
# Deal with unwind.h reference
do_install := "${@d.getVar("do_install").replace("/arm-linux-gnueabihf/gcc/arm-linux-gnueabihf/", "/${TARGET_SYS}/gcc/${TARGET_SYS}/")}"

python () {
    for i in d.getVar("PACKAGES").split():
        v = d.getVar("FILES_" + i, False)
        if v:
            d.setVar("FILES_" + i, v.replace("/${TARGET_SYS}", "/arm-linux-gnueabihf").replace("/${TARGET_PREFIX}", "/arm-linux-gnueabihf-"))
}
