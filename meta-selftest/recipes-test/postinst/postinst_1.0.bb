LICENSE = "MIT"

ALLOW_EMPTY_${PN} = "1"
ALLOW_EMPTY_${PN}-a = "1"
ALLOW_EMPTY_${PN}-b = "1"
ALLOW_EMPTY_${PN}-d = "1"
ALLOW_EMPTY_${PN}-p = "1"
ALLOW_EMPTY_${PN}-t = "1"

PACKAGES =+ "${PN}-a ${PN}-b ${PN}-d ${PN}-p ${PN}-t"
FILES_${PN}-a = ""
FILES_${PN}-b = ""
FILES_${PN}-d = ""
FILES_${PN}-p = ""
FILES_${PN}-t = ""

# Runtime dependencies
RDEPENDS_${PN}-a = "${PN}"
RDEPENDS_${PN}-b = "${PN}-a"
RDEPENDS_${PN}-d = "${PN}-b"
RDEPENDS_${PN}-p = "${PN}-d"
RDEPENDS_${PN}-t = "${PN}-p"

# Main recipe post-install
pkg_postinst_${PN} () {
    tfile="/etc/postinsta-test"
    if test "x$D" != "x" then
        # Need to run on first boot
        exit 1
    else
        echo "lets write postinst" > $tfile
    fi
}

# Dependency recipes post-installs
pkg_postinst_${PN}-a () {
    efile="/etc/postinst-test"
    tfile="/etc/postinsta-test"
    rdeps="postinst"

    if test "x$D" != "x"; then
      # Need to run on first boot
      exit 1
    else
      if test -e $efile ; then
        echo 'success' > $tfile
      else
        echo 'fail to install $rdeps first!' >&2
        exit 1
      fi
   fi
}

pkg_postinst_${PN}-b () {
    efile="/etc/postinsta-test"
    tfile="/etc/postinstb-test"
    rdeps="postinsta"

    if test "x$D" != "x"; then
      # Need to run on first boot
      exit 1
    else
      if test -e $efile ; then
        echo 'success' > $tfile
      else
        echo 'fail to install $rdeps first!' >&2
        exit 1
      fi
   fi
}

pkg_postinst_${PN}-d () {
    efile="/etc/postinstb-test"
    tfile="/etc/postinstd-test"
    rdeps="postinstb"

    if test "x$D" != "x"; then
      # Need to run on first boot
      exit 1
    else
      if test -e $efile ; then
        echo 'success' > $tfile
      else
        echo 'fail to install $rdeps first!' >&2
        exit 1
      fi
   fi
}

pkg_postinst_${PN}-p () {
    efile="/etc/postinstd-test"
    tfile="/etc/postinstp-test"
    rdeps="postinstd"

    if test "x$D" != "x"; then
      # Need to run on first boot
      exit 1
    else
      if test -e $efile ; then
        echo 'success' > $tfile
      else
        echo 'fail to install $rdeps first!' >&2
        exit 1
      fi
   fi
}

pkg_postinst_${PN}-t () {
    efile="/etc/postinstp-test"
    tfile="/etc/postinstt-test"
    rdeps="postinstp"

    if test "x$D" != "x"; then
      # Need to run on first boot
      exit 1
    else
      if test -e $efile ; then
          echo 'success' > $tfile
      else
          echo 'fail to install $rdeps first!' >&2
          exit 1
      fi
   fi
}
