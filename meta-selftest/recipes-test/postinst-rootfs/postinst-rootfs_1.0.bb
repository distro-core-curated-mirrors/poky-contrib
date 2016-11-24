LICENSE = "MIT"

ALLOW_EMPTY_${PN} = "1"

pkg_postinst_${PN} () {
      touch "$D"/this-was-created-at-rootfstime
}
