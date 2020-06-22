require icu.inc

LIC_FILES_CHKSUM = "file://../LICENSE;md5=a3808a5b70071b07f87ff2205e4d75a0"

def icu_download_version(d):
    pvsplit = d.getVar('PV').split('.')
    return pvsplit[0] + "_" + pvsplit[1]

def icu_download_folder(d):
    pvsplit = d.getVar('PV').split('.')
    return pvsplit[0] + "-" + pvsplit[1]

ICU_PV = "${@icu_download_version(d)}"
ICU_FOLDER = "${@icu_download_folder(d)}"

# http://errors.yoctoproject.org/Errors/Details/20486/
ARM_INSTRUCTION_SET_armv4 = "arm"
ARM_INSTRUCTION_SET_armv5 = "arm"

BASE_SRC_URI = "https://github.com/unicode-org/icu/releases/download/release-${ICU_FOLDER}/icu4c-${ICU_PV}-src.tgz"
DATA_SRC_URI = "https://github.com/unicode-org/icu/releases/download/release-${ICU_FOLDER}/icu4c-${ICU_PV}-data.zip"
SRC_URI = "${BASE_SRC_URI};name=code \
           ${DATA_SRC_URI};name=data \
           file://filter.json \
           file://fix-install-manx.patch \
           file://0001-icu-Added-armeb-support.patch \
           file://not-parallel.patch \
           "

SRC_URI_append_class-target = "\
           file://0001-Disable-LDFLAGSICUDT-for-Linux.patch \
          "
SRC_URI[code.sha256sum] = "94a80cd6f251a53bd2a997f6f1b5ac6653fe791dfab66e1eb0227740fb86d5dc"
SRC_URI[data.sha256sum] = "7c16a59cc8c06128b7ecc1dc4fc056b36b17349312829b17408b9e67b05c4a7e"

UPSTREAM_CHECK_REGEX = "icu4c-(?P<pver>\d+(_\d+)+)-src"
UPSTREAM_CHECK_URI = "https://github.com/unicode-org/icu/releases"

EXTRA_OECONF_append_libc-musl = " ac_cv_func_strtod_l=no"
EXTRA_OECONF_append_class-target = " ICU_DATA_FILTER_FILE=${WORKDIR}/filter.json"

# maybe always do this: performance hit?
do_unpack[postfuncs] += "inject_icu_data"
inject_icu_data_class-target() {
    rm -rf ${S}/data
    cp -a ${WORKDIR}/data ${S}
}
inject_icu_data() {
    :
}
