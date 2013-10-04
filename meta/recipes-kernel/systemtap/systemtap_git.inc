LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=b234ee4d69f5fce4486a80fdaf4a4263"

<<<<<<< HEAD
SRCREV = "e58138572ebddac9498b93c76770eeca7d45e3b1"
PV = "2.3+git${SRCPV}"

SRC_URI = "git://sourceware.org/git/systemtap.git \
           file://docproc-build-fix.patch \
           file://obsolete_automake_macros.patch \
=======
SRCREV = "48fa6b5e1d3e636c34cbd5650370e6f634efc294"
PV = "1.8+git${SRCPV}"

SRC_URI = "git://sources.redhat.com/git/systemtap.git;protocol=git \
           file://docproc-build-fix.patch \
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
          "

FILESPATH = "${FILE_DIRNAME}/systemtap"

SRC_URI[md5sum]    = "cb202866ed704c44a876d041f788bdee"
SRC_URI[sha256sum] = "8ffe35caec0d937bd23fd78a3a8d94b58907cc0de0330b35e38f9f764815c459"

# systemtap doesn't support mips
COMPATIBLE_HOST = '(x86_64.*|i.86.*|powerpc.*|arm.*)-linux'

S = "${WORKDIR}/git"

<<<<<<< HEAD
# systemtap can't be built without optimization, if someone tries to compile an
# entire image as -O0, we override it with -O2 here and give a note about it.
def get_optimization(d):
    selected_optimization = d.getVar("SELECTED_OPTIMIZATION", True)
    if base_contains("SELECTED_OPTIMIZATION", "-O0", "x", "", d) == "x":
        bb.note("systemtap can't be built with -O0, -O2 will be used instead.")
        return selected_optimization.replace("-O0", "-O2")
    return selected_optimization

SELECTED_OPTIMIZATION := "${@get_optimization(d)}"

=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
