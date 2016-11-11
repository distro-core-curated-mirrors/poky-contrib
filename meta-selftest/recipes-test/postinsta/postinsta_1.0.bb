LICENSE = "MIT"

RDEPENDS_${PN} = "postinstz"

ALLOW_EMPTY_${PN} = "1"

pkg_postinst_${PN} () {
   if test "x$D" != "x"; then
      # Need to run on first boot
      exit 1
   else
      if test -e /etc/postinstz-test ; then
          echo 'success' > /etc/postinsta-test
      else
          echo 'fail to install postinstz first!' >&2
          exit 1
      fi
   fi
}

