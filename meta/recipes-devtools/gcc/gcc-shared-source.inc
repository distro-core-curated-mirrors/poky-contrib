SRC_URI = ""

do_unpack[depends] += "gcc-source-${PV}:do_preconfigure"
do_populate_lic[depends] += "gcc-source-${PV}:do_unpack"

EXTERNALSRC_pn-${PN} = "${S}"
