DESCRIPTION = "createrepo creates rpm-metadata for rpms to build the repository"
HOMEPAGE = "http://createrepo.baseurl.org/"

LICENSE = "GPLv2+"
LIC_FILES_CHKSUM = "file://COPYING;md5=18810669f13b87348459e611d31ab760"

<<<<<<< HEAD
DEPENDS_class-native += "libxml2-native rpm-native"

PR = "r9"
=======
RDEPENDS_${PN}_virtclass-native += "libxml2-native rpm-native"

PR = "r7"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

SRC_URI= "http://createrepo.baseurl.org/download/${BP}.tar.gz \
          file://fix-native-install.patch \
          file://python-scripts-should-use-interpreter-from-env.patch \
	  file://createrepo-rpm549.patch \
<<<<<<< HEAD
	  file://recommends.patch \
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
	  file://rpm-createsolvedb.py \
         "

SRC_URI[md5sum] = "3e9ccf4abcffe3f49af078c83611eda2"
SRC_URI[sha256sum] = "a73ae11a0dcde8bde36d900bc3f7f8f1083ba752c70a5c61b72d1e1e7608f21b"

BBCLASSEXTEND = "native"

do_install () {
	oe_runmake -e 'DESTDIR=${D}' install
	install -m 0755 ${WORKDIR}/rpm-createsolvedb.py ${D}${bindir}/
}

# Wrap the python script since the native python is
# ${bindir}/python-native/python, and the "#! /usr/bin/env python" can't
# find it since it is not in PATH.
<<<<<<< HEAD
do_install_append_class-native () {
=======
do_install_append_virtclass-native () {
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
	# Not all the python scripts should be wrapped since some of
	# them are modules (be imported).
	for i in ${D}${datadir}/createrepo/genpkgmetadata.py \
		 ${D}${datadir}/createrepo/modifyrepo.py \
		 ${D}${bindir}/rpm-createsolvedb.py ; do
<<<<<<< HEAD
		sed -i -e 's|^#!.*/usr/bin/env python|#! /usr/bin/env nativepython|' $i
=======
		create_wrapper $i ${STAGING_BINDIR_NATIVE}/python-native/python
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
	done

	create_wrapper ${D}/${bindir}/createrepo \
			RPM_USRLIBRPM=${STAGING_LIBDIR_NATIVE}/rpm \
			RPM_ETCRPM=${STAGING_ETCDIR_NATIVE}/rpm \
			RPM_LOCALEDIRRPM=${STAGING_DATADIR_NATIVE}/locale
}
