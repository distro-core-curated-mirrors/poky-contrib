LICENSE = "MIT"

ALLOW_EMPTY_${PN} = "1"

pkg_postinst_${PN} () {
    if [ x"$D" = "x" ]; then
        # Actions to carry out on the device go here
	touch /etc/this-was-created-at-first-boot
    else
          exit 1
    fi
}
