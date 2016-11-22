LICENSE = "MIT"

ALLOW_EMPTY_${PN} = "1"

pkg_postinst_${PN} (){
    if test "x$D" != "x"' then
        # Need to run on first boot
        exit 1
    else
        echo "lets write postinst" > /etc/postinst-test
    fi
}
