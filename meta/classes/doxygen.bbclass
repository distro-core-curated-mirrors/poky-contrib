# Helper class to pull in the right doxygen dependencies and
# enable or disable documentation building (depending on whether 'api-documentation'
# is in DISTRO_FEATURES).

DOXYGEN_ENABLED = "${@bb.utils.contains('DISTRO_FEATURES', 'api-documentation', 'True', 'False', d)}"
DOXYGEN_ENABLE_FLAGS = ""
DOXYGEN_DISABLE_FLAGS = ""

EXTRA_OECONF_prepend_class-target = "${@bb.utils.contains('DOXYGEN_ENABLED', 'True', ${DOXYGEN_ENABLE_FLAGS}, \
                                                                                     ${DOXYGEN_DISABLE_FLAGS}, d)} "

# When building native recipes, disable gtkdoc, as it is not necessary,
# pulls in additional dependencies, and makes build times longer
EXTRA_OECONF_prepend_class-native = ${DOXYGEN_DISABLE_FLAGS}
EXTRA_OECONF_prepend_class-nativesdk = ${DOXYGEN_DISABLE_FLAGS}

DEPENDS_append_class-target = " doxygen-native"

UNKNOWN_CONFIGURE_WHITELIST_append = ${DOXYGEN_DISABLE_FLAGS} ${DOXYGEN_DISABLE_FLAGS}

