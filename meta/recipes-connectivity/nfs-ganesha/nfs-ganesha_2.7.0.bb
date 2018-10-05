# TODO: review licenses
LICENSE = "LGPLv3 & Unknown"
LIC_FILES_CHKSUM = "file://src/LICENSE.txt;md5=e6a600fd5e1d9cbde2d983680233ad02 \
                    file://src/cidr/LICENSE;md5=ab952b9c4b37753b18d79f305e8d8593"

SRC_URI = "https://download.nfs-ganesha.org/2.7/${PV}/${BPN}-${PV}.tar.gz \
           file://module.patch \
           file://uninit.patch"
SRC_URI[md5sum] = "816af386ae38626a06c5ddb06a092fc8"
SRC_URI[sha256sum] = "a458bd461049e4800bad24a2fd01335de6020f46ee495d5b2621eb3270097bca"

DEPENDS = "flex-native bison-native ntirpc util-linux dbus"

inherit cmake pkgconfig

OECMAKE_SOURCEPATH = "${S}/src"

EXTRA_OECMAKE += "-DUSE_SYSTEM_NTIRPC=ON"
# TODO packageconfig
EXTRA_OECMAKE += "-DUSE_GSS=OFF"

# Sort out the brain-dead cmake file
# (https://github.com/nfs-ganesha/ntirpc/issues/150)
do_install_append() {
    if [ "${prefix}/lib64" != "${libdir}" -a -d ${D}${prefix}/lib64 ]; then
        mv ${D}${prefix}/lib64 ${D}${libdir}
    fi

	rm -rf ${D}/var/run
}

FILES_${PN} += "${libdir}/ganesha/*.so"

BBCLASSEXTEND = "native nativesdk"
