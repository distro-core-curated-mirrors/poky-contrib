LICENSE = "MIT"

RDEPENDS_${PN} = "postinst"

ALLOW_EMPTY_${PN} = "1"

pkg_postinst_${PN} () {
   if test "x$D" != "x"; then
      # Need to run on first boot
      exit 1
   else
      if test -e /etc/postinst-test ; then
          echo 'success' > /etc/postinsta-test
      else
          echo 'fail to install postinst first!' >&2
          exit 1
      fi
   fi
}
