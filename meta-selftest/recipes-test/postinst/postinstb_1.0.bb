SUMMARY = "Device formfactor information"
SECTION = "base"
LICENSE = "MIT"

RDEPENDS_${PN} = "postinsta"

ALLOW_EMPTY_${PN} = "1"

pkg_postinst_${PN} () {
   if test "x$D" != "x"; then
      # Need to run on first boot
      exit 1
   else
      if test -e /etc/postinsta-test ; then
          echo 'success' > /etc/postinstb-test
      else
          echo 'fail to install postinsta first!' >&2
          exit 1
      fi
   fi
}
