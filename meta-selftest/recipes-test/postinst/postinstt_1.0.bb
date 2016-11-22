SUMMARY = "Device formfactor information"
SECTION = "base"
LICENSE = "MIT"

RDEPENDS_${PN} = "postinstp"

ALLOW_EMPTY_${PN} = "1"

pkg_postinst_${PN} () {
   if test "x$D" != "x"; then
      # Need to run on first boot
      exit 1
   else
      if test -e /etc/postinstp-test ; then
          echo 'success' > /etc/postinstt-test
      else
          echo 'fail to install postinstp first!' >&2
          exit 1
      fi
   fi
}
